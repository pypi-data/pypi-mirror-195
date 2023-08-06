Qt Dataset Viewer
==========


This module is for debugging ML projects. It is PyQt5 based viewer for torch.utils.dataset.



Installation
------------

Use the package manager `pip` to install ``qtdatasetviewer`` from PyPi.

```bash
pip install qtdatasetviewer
```


Usage
-----

```python
    import sys
    from glob import glob
    from dataset import SampleDataset
    from PyQt5.QtWidgets import QApplication

    from PIL import Image
    from qtdatasetviewer.abstract_convert_to_pil import AbstractConvertToPil
    from qtdatasetviewer.qt_dataset_viewer import run_qt_dataset_viewer

    import torchvision.transforms as T


    class Convert(AbstractConvertToPil):

        def convert(self, item) -> Image:
            image, mask = item
            transform = T.ToPILImage()
            return transform(image)


       
    if __name__ == "__main__":
        dataset = SampleDataset(files=glob("data/*.*"))
        run_qt_dataset_viewer(Convert(dataset))
```


Disclaimer
----------

The package and the code is provided "as-is" and there is NO WARRANTY of any kind. 
Use it only if the content and output files make sense to you.

