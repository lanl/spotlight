# Spotlight Documentation

To auto-generate the Spotlight modules documentation and build HTML pages, do:
```
rm spotlight*.rst
sphinx-apidoc --module-first --full -o . ../spotlight
make html
```

To locally view documentation, do:
```
open _build/html/index.html 
```
