from PyQt5.QtWidgets import QApplication
from model import Image
from view import UIWindow

image = Image()

app = QApplication([])
window = UIWindow(image)
window.show()
app.exit(app.exec_())
