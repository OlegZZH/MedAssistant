// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only
import QtQuick 6.6
import MedAssistant
import QtQuick.Controls 6.6
import QtQuick.Layouts

Window {
    id: window
    width: Constants.width
    height: Constants.height

    visible: true
    color: "#111428"
    title: "MedAssistant"

    ListView {
        id: listView
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: addButton.bottom
        anchors.bottom: parent.bottom
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        anchors.topMargin: 20
        anchors.bottomMargin: 12
        model: ListModel {
            ListElement {
                name: "Grey"
                colorCode: "grey"
            }

            ListElement {
                name: "Red"
                colorCode: "red"
            }

            ListElement {
                name: "Blue"
                colorCode: "blue"
            }

            ListElement {
                name: "Green"
                colorCode: "green"
            }
        }
        delegate: Item {
            x: 5
            width: 80
            height: 40
            Row {
                id: row1
                spacing: 10
                Rectangle {
                    width: 40
                    height: 40
                    color: colorCode
                }

                Text {
                    text: name
                    anchors.verticalCenter: parent.verticalCenter
                    font.bold: true
                }
            }
        }

        CustomModal {
            id: customModal
            x: 179
            y: 588
        }
    }

    Text {
        id: mainTitle
        color: "#ffffff"
        text: qsTr("MedAssistant")
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 12
        font.pixelSize: 40
        horizontalAlignment: Text.AlignHCenter

        Button {
            id: exportButton
            x: 509
            width: 48
            height: 48
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: settingsButton.left
            anchors.rightMargin: 12
            icon.color: "#ffffff"
            icon.source: "images/export.svg"
            display: AbstractButton.IconOnly
            background: Rectangle {
                color: exportButton.down ? "#03040A" : "#00ffffff"
            }
        }

        Button {
            id: settingsButton
            x: 615
            width: 48
            height: 48
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: 12
            icon.color: "#ffffff"
            icon.source: "images/tools.svg"
            display: AbstractButton.IconOnly
            background: Rectangle {
                color: "#00ffffff"
            }
        }
    }

    RoundButton {
        id: addButton
        text: "+"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: mainTitle.bottom
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        anchors.topMargin: 20
        font.pixelSize: 30
        icon.color: "#ffffff"
        opacity: down ? 0.6 : 1
        background: Rectangle {
            color: addButton.down ? "#03040A" : "#111428"
            radius: addButton.radius
            border.color: "#464C6D"
            border.width: 2
        }
        contentItem: Text {
            color: "#ffffff"
            text: addButton.text
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font: addButton.font
        }
        onClicked: {
            addPatientDialog.fillAndOpen()
        }
    }
    CustomModal {
        id: addPatientDialog

        contentItem: AddPatientModal {
            id: addPatientModal
        }
        function fillAndOpen() {
            addPatientDialog.open()
        }
    }
}
