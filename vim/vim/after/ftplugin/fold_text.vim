function! GenericFoldText()
  let foldsize = (v:foldend-v:foldstart)
  let line = substitute(getline(v:foldstart), ' {{{\d', '', 'g')
  return line.' ('.foldsize.' lines)'
endfunction
setlocal foldtext=GenericFoldText()

