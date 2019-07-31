# Spotlight Documentation

To build documentation, do:
```
make html
```

To locally view documentation, do:
```
open _build/html/index.html 
```

To auto-generate the Spotlight modules documentation, do:
```
rm spotlight.rst spotlight.io.rst
sphinx-apidoc -F -o . ../spotlight
```
