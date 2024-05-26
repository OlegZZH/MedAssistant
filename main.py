import os
import sys
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app_dir = Path(__file__).resolve().parent

    os.environ["QT_SCALE_FACTOR"] = str(1)
    os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
    os.environ["QT_VIRTUALKEYBOARD_DESKTOP_DISABLE"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_LOGGING_RULES"] = "qt.qml.connections=true"
    os.environ["QT_QUICK_CONTROLS_CONF"] = f"{app_dir}/view/qtquickcontrols2.conf"
    os.environ["QML_COMPAT_RESOLVE_URLS_ON_ASSIGNMENT"] = "1"

    # Useful for debugging
    # os.environ["QSG_VISUALIZE"] = "batches"
    # os.environ["QSG_VISUALIZE"] = "clip"
    # os.environ["QSG_VISUALIZE"] = "changes"
    # os.environ["QSG_VISUALIZE"] = "overdraw"

    app = QApplication(sys.argv)  # We need to create app before using QThread

    # NOTE:
    # refer to https://stackoverflow.com/a/4939113 (only way to correct handle signal in PyQT)
    exit_timer = QTimer()

    exit_timer.timeout.connect(lambda: None)
    exit_timer.start(1000)

    # med_model = Model()
    # med_controller = Controller(med_model)
    med_view = QQmlApplicationEngine()

    # med_view.rootContext().setContextProperty("med_model", med_model)
    # med_view.rootContext().setContextProperty("med_controller", med_controller)

    med_view.addImportPath(f"{app_dir}/view/imports")
    qml_file = f"{app_dir}/view/content/App.qml"

    med_view.load(str(qml_file))

    # result = med_controller.init()
    # result.status_changed.connect(lambda status: med_controller.post_init() if status else None)
    sys.exit(app.exec())
