import QtQuick 6.6
import QtQuick.Controls 6.6

ComboBox {
    id: customComboBoxWidget
    width: 342
    displayText: currentIndex === -1 ? placeholderText : currentText
    height: 34

    delegate: ItemDelegate {
        width: customComboBoxWidget.width - 8
        contentItem: Text {
            text: modelData
            color: "#FFFFFF"
            font.pixelSize: 20
            verticalAlignment: Text.AlignVCenter
            font.family: "Inter"
        }
        highlighted: customComboBoxWidget.highlightedIndex === index
        background: Rectangle {

            color: "#26293E"
        }
    }

    indicator: Image {
        id: arrow
        width: 24
        height: 24
        visible: true
        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.right

        anchors.rightMargin: 10
        source: "images/dropdown_arrow.svg"
        fillMode: Image.PreserveAspectFit
    }

    contentItem: Text {
        id: text1
        color: customComboBoxWidget.currentIndex === -1 ? "#BDC0CF" : customComboBoxWidget.pressed ? "#939393" : "#FFFFFF"
        anchors.leftMargin: 16
        text: customComboBoxWidget.displayText
        anchors.left: parent.left
        font.pixelSize: 20
        verticalAlignment: Text.AlignVCenter
        font.family: "Inter"
    }

    background: Rectangle {
        id: rectangle
        radius: 4
        border.color: "#464C6D"
        color: "#26293E"
        border.width: 1
    }

    popup: Popup {
        y: customComboBoxWidget.height + 4
        width: customComboBoxWidget.width
        implicitHeight: contentItem.implicitHeight + 8
        padding: 4

        contentItem: ListView {
            implicitHeight: contentHeight
            model: customComboBoxWidget.popup.visible ? customComboBoxWidget.delegateModel : null
            currentIndex: customComboBoxWidget.highlightedIndex

            ScrollIndicator.vertical: ScrollIndicator {}
        }

        background: Rectangle {
            color: "#26293E"
            radius: 4
        }
    }
}
