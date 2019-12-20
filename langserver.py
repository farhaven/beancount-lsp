#!/usr/bin/env python3

from pygls.features import COMPLETION, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_CHANGE, FORMATTING
from pygls.server import LanguageServer
from pygls.types import CompletionItem, CompletionList, CompletionParams, DidOpenTextDocumentParams, DidChangeTextDocumentParams, DocumentFormattingParams

server = LanguageServer()

@server.feature(COMPLETION, trigger_characters=[','])
def completions(params: CompletionParams):
    """Returns completion items."""
    server.show_message("completion: {}".format(params))
    return CompletionList(False, [
        CompletionItem('"'),
        CompletionItem('['),
        CompletionItem(']'),
        CompletionItem('{'),
        CompletionItem('}')
    ])

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(params: DidOpenTextDocumentParams):
	server.show_message("open document {}".format(params))

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: DidChangeTextDocumentParams):
	server.show_message("change document {}".format(params))

@server.feature(FORMATTING)
def formatting(params: DocumentFormattingParams):
	server.show_message("formatting request ignored")

print("Starting beancount LSP")
server.start_io()