import QtQuick 6.6
import MedAssistant 1.0


Rectangle {
    id: modalWindowFrame
    width: 200
    height: 200
    color: "#38ADC4"
    radius: 8
    border.color: color
    border.width: 2

    Rectangle {
        id: content
        color: "#111428"
        radius: 8
        anchors.fill: parent
        anchors.topMargin: 24
        anchors.rightMargin: modalWindowFrame.border.width
        anchors.leftMargin: modalWindowFrame.border.width
        anchors.bottomMargin: modalWindowFrame.border.width
    }
}
