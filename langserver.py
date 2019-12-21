#!/usr/bin/env python3

from pygls.features import COMPLETION, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_CHANGE, FORMATTING, TEXT_DOCUMENT_DID_SAVE
from pygls.server import LanguageServer
from pygls.types import TextEdit, Range, Position, CompletionItem, CompletionList, CompletionParams, DidOpenTextDocumentParams, DidChangeTextDocumentParams, DocumentFormattingParams, DidSaveTextDocumentParams

from beancount import loader
from beancount.core.data import Open

import re

class State:
	entries = None
	errors = None
	options = None
	accounts = []

	def load(self, content):
		entries, errors, options = loader.load_string(content)
		self.entries = entries
		self.errors = errors
		self.options = options
		self.rawDoc = content.splitlines()
		self._updateAccounts()

	def _extractAccount(self, line, offset):
		""" Attempts to extract something that looks like an account (prefix) from line at offset """
		r = re.compile(r'\s')
		startoffsets = []
		for m in r.finditer(line):
			if m.span()[1] > offset:
				continue
			startoffsets.append(m.span()[0])
		if startoffsets:
			index = list(sorted(startoffsets))[-1] + 1
		else:
			index = 0
		match = r.split(line[index:])[0]
		return index, match

	def getAccounts(self, row, character):
		""" Returns a list of accounts that sort of match what's in the loaded document at the given position """
		line = self.rawDoc[row]
		index, pattern = self._extractAccount(line, character)
		# Return all accounts that somehow match the pattern
		matches = [a for a in self.accounts if pattern in a]
		return index, index + len(pattern), matches

	def _updateAccounts(self):
		accs = []
		for e in self.entries:
			if not isinstance(e, Open):
				continue
			accs.append(e.account)
		self.accounts = accs

state = State()

server = LanguageServer()

@server.feature(COMPLETION)
def completions(params: CompletionParams):
    """Returns completion items."""
    start, end, accounts = state.getAccounts(params.position.line, params.position.character)
    line = params.position.line
    items = []
    for a in accounts:
		item = CompletionItem(a)
		item.textEdit = TextEdit(Range(Position(line, start), Position(line, end)), a)
		items.append(item)
    return CompletionList(False, items)

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(params: DidOpenTextDocumentParams):
	state.load(params.textDocument.text)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(params: DidChangeTextDocumentParams):
	state.load(params.contentChanges[0].text)
	if len(params.contentChanges) != 1:
		server.show_message("unexpected number of changes received")

@server.feature(FORMATTING)
def formatting(params: DocumentFormattingParams):
	server.show_message("formatting request ignored")

@server.feature(TEXT_DOCUMENT_DID_SAVE)
def formatting(params: DidSaveTextDocumentParams):
	server.show_message("save request ignored")

server.start_io()