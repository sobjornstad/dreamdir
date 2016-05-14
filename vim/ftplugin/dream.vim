" Dreamdir dream format vim settings
" Copyright 2016 Soren Bjornstad; MIT license.

setlocal tabstop=8
setlocal noexpandtab
setlocal spell
setlocal cpoptions+=J " consider sentences separated by double space
syn sync fromstart " lucid sections often get unhighlighted when they're long otherwise; performance not a concern as dream files are fairly short

nnoremap <LocalLeader>i yi<:silent !xdg-open images/"<CR><C-L>
