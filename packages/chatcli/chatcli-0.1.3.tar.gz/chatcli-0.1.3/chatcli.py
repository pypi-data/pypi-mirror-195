"""
Streaming CLI interface for OpenAI's Chat API.
"""

import io
import sys
from enum import Enum
from typing import *

from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.history import History
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import prompt
from prompt_toolkit.layout import BufferControl
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.layout.containers import Window


import fire
import openai
import pkg_resources
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding import KeyPressEvent
from prompt_toolkit.shortcuts import prompt

T = TypeVar("T", MutableMapping, str)


class ChatGenerator:
    def __init__(
        self,
        messages: Optional[List[Dict[str, str]]] = None,
        *,
        sep: Optional[str] = "\n",
    ) -> None:
        self.messages = messages or [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        self.sep = sep

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def send(self, user_message: str, write: Callable[[str], None]) -> Dict[str, str]:
        assert isinstance(user_message, str)

        # Add the user's message to the list of messages
        self.add_message("user", user_message)

        # Send the messages to the API, accumulate the responses, and print them as they come in
        response_accumulated = None

        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            stream=True,
        ):
            if response_accumulated is None:
                # Set the initial response to the first response (less the delta)
                response_accumulated = response.choices[0]
            else:
                # Apply the delta to the accumulated response
                response_accumulated.delta = string_tree_apply_delta(
                    response_accumulated.delta, response.choices[0].delta
                )
            if "content" in response.choices[0].delta:
                write(response.choices[0].delta.content)

        # Rename the delta to message
        response_accumulated.message = response_accumulated.pop("delta")

        # Apply the separator
        if self.sep is not None:
            write(self.sep)
            response_accumulated.message.content += self.sep

        # Add the response to the list of messages
        assert response_accumulated.message.role == "assistant"
        self.add_message("assistant", response_accumulated.message.content)

        return response_accumulated

    def pop(self) -> MutableMapping:
        """
        Pop the last user message.
        """
        return self.messages.pop()


def string_tree_apply_delta(tree: T, delta: T) -> T:
    """
    Apply a delta to a tree of strings.

    Parameters
    ----------
    tree : T
        The Python tree to apply the delta to.
    delta : T
        The delta to apply to the Python tree.

    Returns
    -------
    T
        The Python tree with the delta applied.
    """
    if isinstance(tree, MutableMapping):
        assert isinstance(delta, MutableMapping)
        for key, value in delta.items():
            if key not in tree:
                tree[key] = value
            else:
                tree[key] = string_tree_apply_delta(tree[key], value)
        return tree
    elif isinstance(tree, str):
        assert isinstance(delta, str)
        return tree + delta
    else:
        raise TypeError(f"Invalid type {type(tree)}")


class PromptCode(Enum):
    UNDO = 1
    REDO = 2


def multiline_prompt(
    default: str = "", *, swap_newline_keys: bool, session: PromptSession
) -> str:
    """
    Prompt the user for a multi-line input.

    Parameters
    ----------
    message : Optional[str]
        The message to display to the user.
    swap_newline_keys : bool
        Whether to swap the keys for submitting and entering a newline.

    Returns
    -------
    str
        The user's input.
    """
    # Define the key bindings
    kb = KeyBindings()

    def enter(event: KeyPressEvent):
        """
        Enter a newline.

        Parameters
        ----------
        event : KeyPressEvent
            The key press event.
        """
        event.current_buffer.insert_text("\n")

    def submit(event: KeyPressEvent):
        """
        Submit the input.

        Parameters
        ----------
        event : KeyPressEvent
            The key press event.
        """
        event.current_buffer.validate_and_handle()

    # Bind them
    if swap_newline_keys:
        kb.add("enter")(enter)
        kb.add("escape", "enter")(submit)
    else:
        kb.add("escape", "enter")(enter)
        kb.add("enter")(submit)

    # Define key bindings for undo and redo
    @kb.add("c-z")
    def undo(event: KeyPressEvent):
        """
        Undo the last user message.

        Parameters
        ----------
        event : KeyPressEvent
            The key press event.
        """
        # Erase the current input
        event.current_buffer.text = ""
        event.app.exit(result=PromptCode.UNDO)

    # Define a prompt continuation function
    def prompt_continuation(width: int, line_number: int, wrap_count: int) -> str:
        """
        Return the continuation prompt.

        Parameters
        ----------
        width : int
            The width of the prompt.
        line_number : int
            The line number of the prompt.
        wrap_count : int
            The number of times the prompt has wrapped.

        Returns
        -------
        str
            The continuation prompt.
        """
        return "... ".rjust(width)

    return session.prompt(
        ">>> ",
        default=default,
        multiline=True,
        key_bindings=kb,
        prompt_continuation=prompt_continuation,
    )


def chatcli(
    *,
    system: str = "You are a helpful assistant.",
    assistant: Optional[str] = None,
    swap_newline_keys: bool = False,
) -> None:
    """
    Chat with an OpenAI API model using the command line.

    Parameters
    ----------
    system : str
        The system message to send to the model.
    assistant : Optional[str]
        The assistant message to send to the model.
    swap_newline_keys : bool
        Whether to swap the keys for submitting and entering a newline.
    """

    # Print a header
    chatcli_version = pkg_resources.get_distribution("chatcli").version
    print(f"ChatCLI v{chatcli_version}", end=" | ")
    if swap_newline_keys:
        print("meta + ↩ submit | ↩ newline")
    else:
        print("↩ : submit | meta + ↩ : newline")

    # Create the list of messages
    messages = [{"role": "system", "content": system}]
    if assistant is not None:
        messages.append({"role": "assistant", "content": assistant})

    # Create prompt_toolkit objects
    session = PromptSession()

    # Create the generator
    chat = ChatGenerator(messages=messages)

    default = ""

    # This is the main loop
    while True:
        # Get the user's message
        user_message = multiline_prompt(
            swap_newline_keys=swap_newline_keys, session=session, default=default
        )

        # Clear the default
        default = ""

        if user_message == PromptCode.UNDO:
            # Undo the prompt
            session.output.cursor_up(1)
            # Undo the message
            while len(chat.messages) > 0 and chat.messages[-1]["role"] in ["user", "assistant"]:
                message = chat.messages.pop()
                # Wind back the prompt
                for _ in message["content"].splitlines():
                    session.output.cursor_up(1)
                if message["role"] == "user":
                    default = message["content"]
                    break
            session.output.erase_down()
            session.output.flush()

        elif user_message == "exit":
            break
        else:
            assert isinstance(user_message, str)

            def write(message: str) -> None:
                """
                Write a message to the console.
                """
                session.output.write_raw(message)
                session.output.flush()

            # Send the user's message to the generator
            chat.send(user_message, write=write)


def test_chatgen() -> None:
    """
    Test the chatgen generator.
    """
    # Create the list of messages
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    # Create the generator
    chat = ChatGenerator(messages)

    # Send the user's message to the generator
    assert "Dodgers" in chat.send("Who won the world series in 2020?")["message"]["content"]
    assert "Texas" in chat.send("Where was it played?")["message"]["content"]


if __name__ == "__main__":
    fire.Fire(chatcli)
