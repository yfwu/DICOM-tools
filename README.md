Usage
-----

Run the anonymizer on a directory of DICOM files:
=======
Default Output Folder (`<input_folder>-anonymized`)

```bash
python cli.py /path/to/input/folder
```

By default the anonymized files are written to `<input_folder>-anonymized`.


To use a specific output directory provide it as the second argument:
=======
The anonymized DICOM files will be written to `/path/to/input/folder-anonymized`.

Custom Output Folder

```bash
python cli.py /path/to/input/folder /path/to/output/folder
```

## Quick Grid Viewer

To preview DICOM folders and select problematic studies for export:

```
python grid_viewer.py /path/to/input/folders /path/to/export/folder
```

Each patient folder (first level inside the input directory) is shown as a thumbnail.
Click a thumbnail to mark it. Marked folders will be copied to the export folder when
pressing the **Export Selected** button.
