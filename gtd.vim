set errorformat=%f:%m
set makeprg=gtd\ --index

" Usage: Gtd <category>
" Or: GtdAllFiles

function! GtdAllFiles()
    set errorformat=%f:%m
    set makeprg=gtd\ --index
    make
endfunction

command! GtdAllFiles call GtdAllFiles()

function! GtdCategory(category)
    set errorformat=%f:%l:%m
    echo a:category
    let &makeprg="gtd -a -e -c " . a:category
    make
endfunction
command! -nargs=1 Gtd :call GtdCategory(<q-args>)

function! GtdOverview()
    " new window
    8new
    0read !gtd -Cn
    setlocal nomodifiable
    setlocal readonly
    setlocal nomodified
    cwindow
    nmap <buffer> g :call GtdCategoryFromFile()<CR>
endfunction
command! GtdOverview call GtdOverview()

function! GtdCategoryFromFile()
    let l=getline(".")
    let data=split(l)
    let category=data[0]
    belowright new
    let curwin=winnr()
    call GtdCategory(category)
    cwindow
    execute curwin . "wincmd w"
endfunction
   

