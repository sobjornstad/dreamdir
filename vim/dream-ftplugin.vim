if exists("drfile_loaded")
 finish
endif
let drfile_loaded = 1

set tabstop=8
set softtabstop=8
set noexpandtab
set spell
set cpoptions+=J " consider sentences separated by double space; testing in dre

function DreamKeywordSearch()
    call inputsave()
    let srch = input('Search term: ')
    call inputrestore()
    execute "/" . srch
    execute ":grep '" . srch . "' *"
endfunction

function DreamHeaderSearch()
    call inputsave()
    let hdr  = input('Header: ')
    let srch = input('Term: ')
    call inputrestore()
    execute "/" . hdr . "\t.*" . srch
    execute ":grep '" . hdr . ":	.*" . srch . "' *"
endfunction

nnoremap <LocalLeader>h :call DreamHeaderSearch()<CR>
nnoremap <LocalLeader>s :call DreamKeywordSearch()<CR>

nnoremap <LocalLeader>t :vs tags.dtags<CR>:set cursorline<CR>
"nnoremap <LocalLeader>dp mz?Id:\t<CR>$by$

"nnoremap <LocalLeader>n ?Id:\t <CR>:noh<CR>$by$:e<C-r>".dre<Home><Right><Right>00<CR>
