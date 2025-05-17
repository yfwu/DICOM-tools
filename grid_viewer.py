import os
import shutil
import argparse
from PIL import Image, ImageTk
import pydicom
import tkinter as tk


THUMB_SIZE = (128, 128)


def find_first_dicom(directory):
    """Return the first DICOM file found within a directory tree."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.dcm'):
                return os.path.join(root, file)
    return None


def load_thumbnail(dicom_path):
    """Load DICOM and return PIL thumbnail and blank flag."""
    try:
        ds = pydicom.dcmread(dicom_path)
        if 'PixelData' not in ds:
            return None, True
        arr = ds.pixel_array
        blank = arr.max() == arr.min()
        img = Image.fromarray(arr)
        img.thumbnail(THUMB_SIZE)
        return img, blank
    except Exception:
        return None, True


class GridViewer(tk.Tk):
    def __init__(self, root_dir, export_dir):
        super().__init__()
        self.title('DICOM Grid Viewer')
        self.root_dir = root_dir
        self.export_dir = export_dir
        self.selected = set()
        self.frames = []
        self._build_ui()

    def _build_ui(self):
        patients = sorted([
            os.path.join(self.root_dir, p)
            for p in os.listdir(self.root_dir)
            if os.path.isdir(os.path.join(self.root_dir, p))
        ])
        cols = 4
        row = col = 0
        for patient in patients:
            dicom_path = find_first_dicom(patient)
            if not dicom_path:
                continue
            image, blank = load_thumbnail(dicom_path)
            if image is None:
                continue
            frame = tk.Frame(self, bd=2, relief='solid', padx=2, pady=2)
            frame.grid(row=row, column=col, padx=5, pady=5)
            img_tk = ImageTk.PhotoImage(image)
            label = tk.Label(frame, image=img_tk)
            label.image = img_tk  # keep reference
            label.pack()
            name = os.path.basename(patient)
            if blank:
                name += ' (blank)'
            text = tk.Label(frame, text=name)
            text.pack()
            frame.bind('<Button-1>', lambda e, p=patient, f=frame: self.toggle(p, f))
            label.bind('<Button-1>', lambda e, p=patient, f=frame: self.toggle(p, f))
            text.bind('<Button-1>', lambda e, p=patient, f=frame: self.toggle(p, f))
            self.frames.append((patient, frame))
            col += 1
            if col >= cols:
                col = 0
                row += 1
        btn = tk.Button(self, text='Export Selected', command=self.export_selected)
        btn.grid(row=row + 1, column=0, columnspan=cols, pady=10)

    def toggle(self, patient, frame):
        if patient in self.selected:
            self.selected.remove(patient)
            frame.config(bg='white')
        else:
            self.selected.add(patient)
            frame.config(bg='yellow')

    def export_selected(self):
        for patient in self.selected:
            name = os.path.basename(patient)
            dst = os.path.join(self.export_dir, name)
            shutil.copytree(patient, dst, dirs_exist_ok=True)
        print(f'Exported {len(self.selected)} patients to {self.export_dir}')


def main():
    parser = argparse.ArgumentParser(description='Quickly preview DICOM folders.')
    parser.add_argument('input', help='Root folder containing patient folders')
    parser.add_argument('output', help='Folder to export selected cases')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    viewer = GridViewer(args.input, args.output)
    viewer.mainloop()


if __name__ == '__main__':
    main()
