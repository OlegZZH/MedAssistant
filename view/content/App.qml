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
    property bool delModeEnabled: false

    ListView {
        id: listView
        property var patientGroup: []

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: addButton.bottom
        anchors.bottom: bottomButtons.top
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        anchors.topMargin: 20
        anchors.bottomMargin: 12
        clip: true
        spacing: 10
        model: med_model.patient_list
        delegate: DropDownBlockWidget {
            titleText: model.patient_name
            ageFieldWidgetInputText: model.age
            sexFieldWidget.current: sexFieldWidget.comboModel.indexOf(model.sex)
            cholesterolLevelFieldWidget.current: cholesterolLevelFieldWidget.comboModel.indexOf(model.cholesterol_level)
            bloodPressureFieldWidget.current: bloodPressureFieldWidget.comboModel.indexOf(model.blood_pressure)
            difficultyBreathingCheckBoxWidgetChecked: model.difficulty_breathing
            fatigueCheckBoxWidgetChecked: model.fatigue
            coughCheckBoxWidgetChecked: model.cough
            feverCheckBoxWidgetChecked: model.fever
            diseaseText: model.disease
            checkable: delModeEnabled
            onCheckedChanged: {
                if (checked) {
                    listView.patientGroup.push(model.patient_id)
                } else {
                    listView.patientGroup.pop(model.patient_id)
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
            anchors.right: binButton.left
            anchors.rightMargin: 12
            icon.color: "#ffffff"
            icon.source: "images/export.svg"
            display: AbstractButton.IconOnly
            background: Rectangle {
                color: exportButton.down ? "#03040A" : "#00ffffff"
            }
        }

        Button {
            id: binButton
            x: 615
            width: 48
            height: 48
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: 12
            icon.color: "#ffffff"
            icon.source: "images/bin.png"
            display: AbstractButton.IconOnly
            background: Rectangle {
                color: binButton.down ? "#03040A" : "#00ffffff"
            }
            onClicked: {
                delModeEnabled = !delModeEnabled
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
        radius: 14
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

    Item {
        id: bottomButtons
        y: 851
        height: 64
        visible: delModeEnabled
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: 12
        anchors.rightMargin: 12
        anchors.bottomMargin: 12

        OkButtonWidget {
            id: okButtonWidget
            text: "Delete"
            enabled: listView.count > 0

            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.horizontalCenter
            anchors.right: parent.right
            anchors.leftMargin: 10
            anchors.rightMargin: 0
            onClicked: {
                med_controller.remove_patients(listView.patientGroup)
                delModeEnabled = false
            }
        }

        ButtonWithTextWidget {
            id: buttonWithTextWidget
            height: 64
            text: "Close"
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.right: parent.horizontalCenter
            anchors.leftMargin: 0
            anchors.rightMargin: 10
            borderRadius: 12
            onClicked: {
                delModeEnabled = false
            }
        }
    }
}
