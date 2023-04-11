# Filter bibliography
To filter out bibliography entries in BibTex format from LaTex files:
1. Filtered `.bib` file for each `.tex` file:
    Run:
    ```bash
    $ python filterbib.py <texfile_1.tex> ... <texfile_n.tex> <bibfile_1.bib> ... <bibfile_n.tex>
    ```
   * Extract all \cite{} entries from each `<texfile_i.tex>`
   * Look for corresponding entries in all the `<bibfile_i.bib>`
   * `<texfile_i_filter.bib>` will contain the filtered bibliography for `<texfile_n.tex>`
2. Filtered `.bib` file for all `.tex` files:
    Run:
    ```bash
    $ python filterbib.py <texfile_1.tex> ... <texfile_n.tex> <bibfile_1.bib> ... <bibfile_n.tex>
                    -m <texmerged_filter.bib>
                    // or
                    --merge-tex <texmerged_filter.bib>
    ```
   * Extract all \cite{} entries from all `<texfile_i.tex>`
   * Look for corresponding entries in all the `<bibfile_i.bib>`
   * `<texmerged_filter.bib>` will contain the filtered bibliography from all the merged `.tex` files