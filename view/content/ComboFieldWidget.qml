import QtQuick 6.6
import QtQuick.Controls 6.6

Item {
    id: comboFieldWidget
    height: comboBox.height + fieldName1.height + 8
    property alias currentText: comboBox.currentText
    property alias comboBoxEnabled: comboBox.enabled
    width: comboBox.width
    property string fieldTitle: "Name"
    property alias comboModel: comboBox.model
    property alias current: comboBox.currentIndex
    property bool necessarily: false
    property string placeholderText: qsTr("Please Choose...")

    Text {
        id: fieldName1
        color: "#BDC0CF"
        text: fieldTitle
        font.pixelSize: 16
        font.family: "Inter"
    }
    ComboBoxWidget {
        id: comboBox
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: fieldName1.bottom
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 8
    }

    Text {
        id: text2
        visible: necessarily
        color: "#E80909"
        text: qsTr("*")
        anchors.left: fieldName1.right
        anchors.top: parent.top
        font.family: "Inter"
        font.pixelSize: 18
        anchors.leftMargin: 2
        anchors.topMargin: 0
    }
}
