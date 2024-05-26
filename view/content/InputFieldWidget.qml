import QtQuick 6.6
import QtQuick.Controls 6.6

Item {
    id: inputFieldWidget
    width: 342
    height: fieldName.height + inputBg.height + 8
    property alias textInputReadOnly: textInput.readOnly
    property alias fieldName: fieldName.text
    property alias unitText: unit.text
    property alias inputText: textInput.text
    property alias placeholderText: textInput.placeholderText
    property alias inputHints: textInput.inputMethodHints
    property alias inputMask: textInput.inputMask
    property bool necessarily: false

    property bool unitVisible: false

    Text {
        id: fieldName
        color: "#BDC0CF"
        text: "Name"
        font.pixelSize: 16
        font.family: "Inter"
    }
    Text {
        id: necessarilyLabel
        visible: necessarily
        color: "#E80909"
        text: qsTr("*")
        anchors.left: fieldName.right
        anchors.top: parent.top
        font.family: "Inter"
        font.pixelSize: 18
        anchors.leftMargin: 2
        anchors.topMargin: 0
    }
    Rectangle {
        id: inputBg

        height: 34

        radius: 4
        color: "#26293E"
        border.color: "#464C6D"
        border.width: 1
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: fieldName.bottom
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 8
        TextField {
            id: textInput
            width: 263
            leftPadding: 0
            color: textInput.readOnly ? "#64687E" : "#FFFFFF"
            text: "Input Text"
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            font.pixelSize: 20
            anchors.bottomMargin: 0
            anchors.topMargin: 0
            anchors.leftMargin: 16
            font.family: "Inter"
            placeholderTextColor: "#BDC0CF"
            background: Rectangle {
                color: "#00ffffff"
                border.color: "#00000000"
            }
        }

        Text {
            id: unit
            x: 296
            visible: unitVisible
            color: textInput.readOnly ? "#64687E" : "#FFFFFF"
            text: "unit"
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            font.pixelSize: 20
            font.family: "Inter"
            anchors.rightMargin: 16
        }
    }
}
