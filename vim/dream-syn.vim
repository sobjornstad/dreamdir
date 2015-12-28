" Vim syntax file
" Dream files

if exists("b:current_syntax")
     finish
endif

let b:current_syntax = "dream"

" headers
syntax match Property "^Id:\t"
syntax match Property "^Date:\t"
syntax match Property "^Lcd:\t"
syntax match Property "^Tags:\t"
syntax match Property "^People:\t"
syntax match Property "^Time:\t"
syntax match Property "^Places:\t"

""" dream formatting """
" lucid sections
syntax region Lucid start="{" end="}" contains=Emphasis,WL,Raw

" backticks
syntax match Raw "\`.\{-\}\`" contained
syntax match Raw "\`.\{-\}\`"

" RL brackets
syntax match WL "\[.\{-\}\]" contained
syntax match WL "\[.\{-\}\]"

" emphasis
syntax match Emphasis "\*.\{-\}\*" contained
syntax match Emphasis "_.\{-\}_" contained
syntax match Emphasis "\*.\{-\}\*"
syntax match Emphasis "_.\{-\}_"

hi link Lucid Underlined
hi link Property Keyword
hi link Raw PreProc
hi link WL Comment
hi link Emphasis Formatted
hi Formatted cterm=bold
