import QtQuick 6.6
import QtQuick.Controls 6.6

CheckBox {
    id: customCheckBox
    width: 132
    text: "Check Box"
    implicitHeight: 20
    font.family: "Inter"
    enabled: true
    checked: false
    property string checkedImage: "images/checked.svg"

    indicator: Item {
        implicitWidth: customCheckBox.height
        implicitHeight: customCheckBox.height
        x: customCheckBox.leftPadding

        width: customCheckBox.height
        height: customCheckBox.height
        anchors.verticalCenter: parent.verticalCenter

        Image {
            anchors.fill: parent

            source: {
                if (customCheckBox.enabled)
                    return customCheckBox.checked ? checkedImage : "images/unchecked.svg"
                else
                    return customCheckBox.checked ? "images/check_box_checked_and_inactive.svg" : "images/check_box_inactive.svg"
            }
            sourceSize.height: 40
            sourceSize.width: 40
        }
    }

    contentItem: Text {
        text: customCheckBox.text
        font: customCheckBox.font

        color: customCheckBox.enabled ? "#FFFFFF" : "#64687E"
        verticalAlignment: Text.AlignVCenter
        leftPadding: customCheckBox.indicator.width + customCheckBox.spacing
    }
}
