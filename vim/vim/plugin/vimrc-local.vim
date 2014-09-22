
" Do we have a local vimrc?
if filereadable('.vimrc.local')
	" If so, source it 
	source .vimrc.local
endif
