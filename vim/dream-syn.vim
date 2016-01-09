" Vim syntax file
" Dream files

if exists("b:current_syntax")
     finish
endif
let b:current_syntax = "dream"

" headers / attributes
syntax match Property "^.\{-\}:\t"

" lucid sections
syntax region Lucid start="{" end="}" contains=Emphasis,WL,Raw

" RL brackets
syntax region WL start="\[" end="\]" contained
syntax region WL start="\[" end="\]"

" backticks
syntax match Raw "\`.\{-\}\`" contained
syntax match Raw "\`.\{-\}\`"

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
