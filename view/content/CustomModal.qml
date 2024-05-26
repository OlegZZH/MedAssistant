import QtQuick 6.6

import QtQuick.Window 2.15
import QtQuick.Controls 6.6

Popup {
    id: customModal
    x: (window.width - width) / 2
    y: (window.height - height) / 2
    modal: true
    padding: 0
    closePolicy: Popup.NoAutoClose
    background: Rectangle {
        color: "#00ffffff"
        border.width: 0
    }
}
