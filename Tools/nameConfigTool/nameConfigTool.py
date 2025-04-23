#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
nameConfigTool - Naming 설정을 GUI로 관리하는 도구
NamingConfig 클래스를 이용하여 JSON 파일을 로드, 편집하고 저장할 수 있는 기능 제공
"""

import sys
import os
import json
from typing import Dict, List, Optional, Any, Tuple

# 상위 디렉토리 경로를 모듈 검색 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# PySide2 라이브러리 임포트
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QListWidget, QListWidgetItem, QComboBox, 
                               QFileDialog, QGroupBox, QTabWidget, QTextEdit,
                               QSpinBox, QTableWidget, QTableWidgetItem, 
                               QHeaderView, QAbstractItemView, QMessageBox,
                               QRadioButton, QButtonGroup, QInputDialog, QCheckBox)
from PySide2.QtCore import Qt, QMimeData, QSize
from PySide2.QtGui import QDrag, QColor

# JalLib 모듈 임포트
from JalLib.namingConfig import NamingConfig
from JalLib.namePart import NamePart, NamePartType

class DraggableListWidget(QListWidget):
    """드래그 앤 드롭을 지원하는 리스트 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        
    def dropEvent(self, event):
        """드롭 이벤트 처리 - 아이템 순서 재배치"""
        super().dropEvent(event)
        
        # 메인 윈도우 찾기
        main_window = None
        parent = self.parent()
        
        # 부모 위젯 트리를 탐색하여 NameConfigToolUI 인스턴스 찾기
        while parent:
            if isinstance(parent, NameConfigToolUI):
                main_window = parent
                break
            parent = parent.parent()
        
        # 메인 윈도우를 찾았으면 updatePartOrder 메서드 호출
        if main_window and hasattr(main_window, 'updatePartOrder'):
            main_window.updatePartOrder()

class NamePartWidget(QWidget):
    """NamePart를 표시하고 편집하는 위젯"""
    
    def __init__(self, part: NamePart, parent=None, color=None):
        super().__init__(parent)
        self.part = part
        self.color = color if color else QColor(150, 150, 150)  # 기본 회색
        self.setupUI()
        
    def setupUI(self):
        """위젯 UI 구성"""
        layout = QVBoxLayout(self)
        
        # 배경색 설정
        self.setAutoFillBackground(True)
        palette = self.palette()
        bg_color = QColor(self.color)
        bg_color.setAlpha(40)  # 투명도 설정
        palette.setColor(self.backgroundRole(), bg_color)
        self.setPalette(palette)
        
        # 테두리 스타일 설정
        border_style = f"border: 2px solid {self.color.name()}; border-radius: 5px;"
        self.setStyleSheet(border_style)
        
        # NamePart 이름 표시
        nameLabel = QLabel(self.part.get_name())
        nameLabel.setAlignment(Qt.AlignCenter)
        nameLabel.setStyleSheet(f"color: {self.color.darker(120).name()}; font-weight: bold; border: none;")
        
        # NamePart 타입 표시
        typeLabel = QLabel(f"({self.part.get_type().name})")
        typeLabel.setAlignment(Qt.AlignCenter)
        typeLabel.setStyleSheet("border: none;")
        
        # 값 선택 드롭다운
        self.valueCombo = QComboBox()
        self.valueCombo.setStyleSheet("border: 1px solid gray;")
        
        # NamePart 타입에 따라 다르게 처리
        if self.part.is_realname():
            self.valueCombo.addItem("이름")
            self.valueCombo.setEnabled(False)
        elif self.part.is_index():
            self.valueCombo.addItem("인덱스")
            self.valueCombo.setEnabled(False)
        else:
            # 사전 정의된 값과 설명을 드롭다운에 추가
            values = self.part.get_predefined_values()
            descriptions = self.part.get_descriptions()
            
            for i, desc in enumerate(descriptions):
                if i < len(values):
                    # 설명과 값을 같이 표시 (설명(값) 형식)
                    self.valueCombo.addItem(f"{desc} ({values[i]})", values[i])
        
        # 위젯 배치
        layout.addWidget(nameLabel)
        layout.addWidget(typeLabel)
        layout.addWidget(self.valueCombo)
        
    def getValue(self) -> str:
        """선택된 값 반환"""
        if self.part.is_realname():
            return "Name"
        elif self.part.is_index():
            return "01"
        else:
            # 현재 선택된 항목의 사용자 데이터(실제 값) 반환
            return self.valueCombo.currentData()
    
    def getNamePart(self) -> NamePart:
        """NamePart 객체 반환"""
        return self.part
        
    def getColor(self) -> QColor:
        """색상 반환"""
        return self.color

class NameConfigToolUI(QMainWindow):
    """네이밍 설정 도구 메인 UI 클래스"""
    
    def __init__(self):
        super().__init__()
        
        # 설정 객체 초기화
        self.configObj = NamingConfig()
        self.currentFilePath = ""
        
        # 미리보기용 기본 이름
        self.previewName = "Name01"
        
        # 필터링 문자 (기본값은 '_')
        self.filteringChar = "_"
        
        # 색상 팔레트 - NamePart 색상 지정용
        self.colorPalette = {
            NamePartType.PREFIX: QColor(70, 150, 195),   # 청록색 계열
            NamePartType.SUFFIX: QColor(160, 110, 190),  # 보라색 계열
            NamePartType.REALNAME: QColor(80, 170, 90),  # 녹색 계열
            NamePartType.INDEX: QColor(215, 120, 70),    # 주황색 계열
            NamePartType.UNDEFINED: QColor(150, 150, 150) # 회색
        }
        
        # NamePart별 고유 색상 저장
        self.partColors = {}
        
        # UI 구성
        self.setupUI()
        
        # 기본 설정 로드
        self.loadDefaultConfig()
        
    def setupUI(self):
        """UI 구성"""
        self.setWindowTitle("Naming Config Tool")
        self.resize(800, 600)
        
        # 메인 위젯 및 레이아웃
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)
        
        # === 파일 관리 영역 ===
        self.setupFileManagementArea()
        
        # === 미리보기 영역 ===
        self.setupPreviewArea()
        
        # === 필터링 문자 영역 ===
        self.setupFilteringCharArea()
        
        # === 인덱스 설정 영역 ===
        self.setupIndexSettingsArea()
        
        # === NameParts 영역 ===
        self.setupNamePartsArea()
        
        # === 편집 영역 ===
        self.setupEditingArea()
        
    def setupFileManagementArea(self):
        """파일 관리 영역 구성"""
        fileGroup = QGroupBox("설정 파일 관리")
        fileLayout = QHBoxLayout(fileGroup)
        
        # 현재 파일 경로
        self.filePathLabel = QLabel("파일: 기본 설정")
        
        # 버튼들
        self.loadButton = QPushButton("불러오기")
        self.saveButton = QPushButton("저장")
        self.saveAsButton = QPushButton("다른 이름으로 저장")
        
        # 이벤트 연결
        self.loadButton.clicked.connect(self.loadConfig)
        self.saveButton.clicked.connect(self.saveConfig)
        self.saveAsButton.clicked.connect(self.saveConfigAs)
        
        # 레이아웃 구성
        fileLayout.addWidget(self.filePathLabel, 1)
        fileLayout.addWidget(self.loadButton)
        fileLayout.addWidget(self.saveButton)
        fileLayout.addWidget(self.saveAsButton)
        
        self.mainLayout.addWidget(fileGroup)
    
    def setupPreviewArea(self):
        """미리보기 영역 구성"""
        previewGroup = QGroupBox("이름 미리보기")
        previewLayout = QHBoxLayout(previewGroup)
        
        # 미리보기 레이블
        self.previewLabel = QLabel(self.previewName)
        self.previewLabel.setAlignment(Qt.AlignCenter)
        self.previewLabel.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        previewLayout.addWidget(self.previewLabel)
        
        self.mainLayout.addWidget(previewGroup)
        
    def setupFilteringCharArea(self):
        """필터링 문자 선택 영역 구성"""
        filterGroup = QGroupBox("구분 문자 설정")
        filterLayout = QHBoxLayout(filterGroup)
        
        # 라디오 버튼으로 선택 구성
        self.filterCharGroup = QButtonGroup(self)
        
        self.underscoreRadio = QRadioButton("밑줄(_)")
        self.underscoreRadio.setChecked(True)  # 기본값으로 설정
        self.filterCharGroup.addButton(self.underscoreRadio)
        
        self.spaceRadio = QRadioButton("공백( )")
        self.filterCharGroup.addButton(self.spaceRadio)
        
        # 선택 이벤트 연결
        self.underscoreRadio.clicked.connect(self.updateFilteringChar)
        self.spaceRadio.clicked.connect(self.updateFilteringChar)
        
        # 레이아웃에 추가
        filterLayout.addWidget(QLabel("구분 문자:"))
        filterLayout.addWidget(self.underscoreRadio)
        filterLayout.addWidget(self.spaceRadio)
        filterLayout.addStretch(1)
        
        self.mainLayout.addWidget(filterGroup)
    
    def setupIndexSettingsArea(self):
        """인덱스 설정 영역 구성"""
        indexGroup = QGroupBox("인덱스 설정")
        indexLayout = QHBoxLayout(indexGroup)
        
        indexLayout.addWidget(QLabel("인덱스 자릿수:"))
        self.paddingSpinBox = QSpinBox()
        self.paddingSpinBox.setMinimum(1)
        self.paddingSpinBox.setMaximum(10)
        self.paddingSpinBox.setValue(2)
        self.paddingSpinBox.valueChanged.connect(self.updatePaddingNum)
        
        indexLayout.addWidget(self.paddingSpinBox)
        indexLayout.addStretch(1)
        
        self.mainLayout.addWidget(indexGroup)
    
    def setupNamePartsArea(self):
        """NameParts 영역 구성"""
        partsGroup = QGroupBox("NamePart")
        partsLayout = QVBoxLayout(partsGroup)
        
        # 안내 레이블
        infoLabel = QLabel("아래 요소들을 드래그하여 순서를 변경할 수 있습니다.")
        infoLabel.setAlignment(Qt.AlignCenter)
        
        # 버튼 레이아웃
        buttonLayout = QHBoxLayout()
        
        # 추가 및 제거 버튼
        self.addPartButton = QPushButton("NamePart 추가")
        self.removePartButton = QPushButton("NamePart 제거")
        
        # 이벤트 연결
        self.addPartButton.clicked.connect(self.addNamePart)
        self.removePartButton.clicked.connect(self.removeNamePart)
        
        buttonLayout.addWidget(self.addPartButton)
        buttonLayout.addWidget(self.removePartButton)
        
        # 드래그 가능한 리스트 위젯
        self.partsList = DraggableListWidget(self)
        self.partsList.setMinimumHeight(150)
        
        # 아이템 선택 이벤트 연결
        self.partsList.itemClicked.connect(self.onPartItemSelected)
        
        partsLayout.addWidget(infoLabel)
        partsLayout.addLayout(buttonLayout)
        partsLayout.addWidget(self.partsList)
        
        self.mainLayout.addWidget(partsGroup)
    
    def setupEditingArea(self):
        """편집 영역 구성"""
        editGroup = QGroupBox("NamePart 편집")
        mainEditLayout = QVBoxLayout(editGroup)  # 전체 레이아웃을 QGroupBox에 직접 설정
        
        # 가로로 나란히 배치할 레이아웃
        editLayout = QHBoxLayout()
        
        # === 기본 정보 영역 ===
        basicGroup = QGroupBox("기본 정보")
        basicLayout = QVBoxLayout(basicGroup)
        
        # 부분 이름 및 타입
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(QLabel("이름:"))
        self.partNameEdit = QLineEdit()
        nameLayout.addWidget(self.partNameEdit, 1)
        
        nameLayout.addWidget(QLabel("타입:"))
        self.partTypeCombo = QComboBox()
        for type_name in [t.name for t in NamePartType]:
            self.partTypeCombo.addItem(type_name)
        nameLayout.addWidget(self.partTypeCombo)
        
        basicLayout.addLayout(nameLayout)
        
        # Direction 체크박스 추가
        directionLayout = QHBoxLayout()
        self.directionCheckBox = QCheckBox("Direction")
        self.directionCheckBox.setToolTip("NamePart가 방향성을 가지는지 여부를 설정합니다 (예: Left/Right, Front/Back)")
        directionLayout.addWidget(self.directionCheckBox)
        directionLayout.addStretch(1)
        
        basicLayout.addLayout(directionLayout)
        basicLayout.addStretch(1)
        
        # === 값 편집 영역 ===
        valuesGroup = QGroupBox("사전 정의 값")
        valuesLayout = QVBoxLayout(valuesGroup)
        
        # 테이블로 값과 설명 편집
        self.valuesTable = QTableWidget(0, 2)
        self.valuesTable.setHorizontalHeaderLabels(["값", "설명"])
        self.valuesTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 버튼 그룹
        valuesButtonLayout = QHBoxLayout()
        self.addValueButton = QPushButton("값 추가")
        self.removeValueButton = QPushButton("값 삭제")
        valuesButtonLayout.addWidget(self.addValueButton)
        valuesButtonLayout.addWidget(self.removeValueButton)
        
        # 이벤트 연결
        self.addValueButton.clicked.connect(self.addValue)
        self.removeValueButton.clicked.connect(self.removeValue)
        self.partTypeCombo.currentIndexChanged.connect(self.updatePartTypeUI)
        
        valuesLayout.addWidget(self.valuesTable)
        valuesLayout.addLayout(valuesButtonLayout)
        
        # 영역 추가
        editLayout.addWidget(basicGroup, 1)  # 1:1 비율로 공간 분배
        editLayout.addWidget(valuesGroup, 1)
        
        # 변경 적용 버튼을 위한 레이아웃
        buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("변경 적용")
        self.applyButton.clicked.connect(self.applyChanges)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.applyButton)
        
        # 메인 레이아웃에 추가
        mainEditLayout.addLayout(editLayout)
        mainEditLayout.addLayout(buttonLayout)
        
        self.mainLayout.addWidget(editGroup)
    
    def loadDefaultConfig(self):
        """기본 설정 로드"""
        try:
            # 기본 설정 로드
            self.configObj = NamingConfig()
            success = self.configObj.load()
            
            if success:
                self.updateUI()
                self.filePathLabel.setText("파일: 기본 설정")
            else:
                QMessageBox.warning(self, "경고", "기본 설정을 로드할 수 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"기본 설정 로드 중 오류 발생: {str(e)}")
    
    def loadConfig(self):
        """설정 파일 불러오기"""
        try:
            # 파일 다이얼로그로 JSON 파일 선택
            filePath, _ = QFileDialog.getOpenFileName(
                self, "설정 파일 불러오기", "", "JSON 파일 (*.json)"
            )
            
            if filePath:
                # 선택한 파일 로드
                success = self.configObj.load(filePath)
                
                if success:
                    self.currentFilePath = filePath
                    self.filePathLabel.setText(f"파일: {os.path.basename(filePath)}")
                    self.updateUI()
                else:
                    QMessageBox.warning(self, "경고", "설정 파일을 로드할 수 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"설정 로드 중 오류 발생: {str(e)}")
    
    def saveConfig(self):
        """현재 설정 저장"""
        try:
            if self.currentFilePath:
                # 기존 경로에 저장
                success = self.configObj.save(self.currentFilePath)
                
                if success:
                    QMessageBox.information(self, "알림", "설정이 저장되었습니다.")
                else:
                    QMessageBox.warning(self, "경고", "설정을 저장할 수 없습니다.")
            else:
                # 경로가 없으면 다른 이름으로 저장
                self.saveConfigAs()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"설정 저장 중 오류 발생: {str(e)}")
    
    def saveConfigAs(self):
        """설정을 새 파일로 저장"""
        try:
            # 파일 다이얼로그로 저장 경로 선택
            filePath, _ = QFileDialog.getSaveFileName(
                self, "설정 파일 저장", "", "JSON 파일 (*.json)"
            )
            
            if filePath:
                # 선택한 경로에 저장
                if not filePath.lower().endswith('.json'):
                    filePath += '.json'
                
                success = self.configObj.save(filePath)
                
                if success:
                    self.currentFilePath = filePath
                    self.filePathLabel.setText(f"파일: {os.path.basename(filePath)}")
                    QMessageBox.information(self, "알림", "설정이 저장되었습니다.")
                else:
                    QMessageBox.warning(self, "경고", "설정을 저장할 수 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"설정 저장 중 오류 발생: {str(e)}")
    
    def updateUI(self):
        """UI 전체 업데이트"""
        # 패딩 값 업데이트
        self.paddingSpinBox.setValue(self.configObj.padding_num)
        
        # 필터링 문자 업데이트
        if self.filteringChar == "_":
            self.underscoreRadio.setChecked(True)
        else:
            self.spaceRadio.setChecked(True)
        
        # 파트 리스트 업데이트
        self.updatePartsList()
        
        # 미리보기 업데이트
        self.updatePreview()
    
    def updateFilteringChar(self):
        """필터링 문자 업데이트"""
        if self.underscoreRadio.isChecked():
            self.filteringChar = "_"
        else:
            self.filteringChar = " "
        
        # 미리보기 업데이트
        self.updatePreview()
    
    def addNamePart(self):
        """새 NamePart 추가"""
        # 이름 입력 다이얼로그
        part_name, ok = QInputDialog.getText(
            self, "NamePart 추가", "새 NamePart 이름을 입력하세요:"
        )
        
        if ok and part_name:
            # 이미 존재하는 이름인지 확인
            if self.configObj.get_part(part_name):
                QMessageBox.warning(self, "경고", f"'{part_name}' NamePart가 이미 존재합니다.")
                return
                
            # 기본 타입으로 PREFIX 사용
            # 기본 값과 설명 하나씩 추가
            success = self.configObj.add_part(
                part_name, 
                NamePartType.PREFIX,
                [f"V{len(self.configObj.name_parts) + 1}"],
                [f"Value {len(self.configObj.name_parts) + 1}"]
            )
            
            if success:
                self.updatePartsList()
                self.updatePreview()
            else:
                QMessageBox.warning(self, "경고", "NamePart 추가에 실패했습니다.")
    
    def removeNamePart(self):
        """선택한 NamePart 제거"""
        # 현재 선택된 아이템
        selected_items = self.partsList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "경고", "제거할 NamePart를 선택하세요.")
            return
        
        selected_item = selected_items[0]
        widget = self.partsList.itemWidget(selected_item)
        part = widget.getNamePart()
        part_name = part.get_name()
        
        # 필수 부분인지 확인
        if part_name in self.configObj.required_parts:
            QMessageBox.warning(self, "경고", f"'{part_name}'은(는) 필수 NamePart이므로 제거할 수 없습니다.")
            return
        
        # 확인 메시지
        reply = QMessageBox.question(
            self, "확인", f"'{part_name}' NamePart를 제거하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # NamePart 제거
            success = self.configObj.remove_part(part_name)
            
            if success:
                self.updatePartsList()
                self.updatePreview()
                QMessageBox.information(self, "알림", f"'{part_name}' NamePart가 제거되었습니다.")
            else:
                QMessageBox.warning(self, "경고", "NamePart 제거에 실패했습니다.")
    
    def updatePartsList(self):
        """NameParts 리스트 업데이트"""
        self.partsList.clear()
        
        for name in self.configObj.get_part_order():
            part = self.configObj.get_part(name)
            if part:
                # 각 NamePart에 대한 고유 색상 가져오기 (없으면 새로 생성)
                if name not in self.partColors:
                    self.partColors[name] = self.generateRandomColor()
                
                color = self.partColors[name]
                
                # 각 NamePart를 위젯으로 변환하여 표시
                partWidget = NamePartWidget(part, color=color)
                partWidget.valueCombo.currentIndexChanged.connect(self.updatePreview)
                
                # 리스트 아이템 생성
                item = QListWidgetItem(self.partsList)
                self.partsList.addItem(item)
                item.setSizeHint(partWidget.sizeHint())
                self.partsList.setItemWidget(item, partWidget)
    
    def generateRandomColor(self) -> QColor:
        """랜덤 색상 생성 (가시성 좋은 색상으로 제한)"""
        import random
        
        # 미리 정의된 보기 좋은 색상 팔레트 (색상 라이브러리에서 자주 사용되는 색상들)
        predefined_colors = [
            QColor(231, 76, 60),   # 밝은 적색
            QColor(52, 152, 219),  # 밝은 청색
            QColor(46, 204, 113),  # 녹색
            QColor(155, 89, 182),  # 보라색
            QColor(241, 196, 15),  # 노란색
            QColor(230, 126, 34),  # 주황색
            QColor(52, 73, 94),    # 어두운 청록색
            QColor(26, 188, 156),  # 청록색
            QColor(243, 156, 18),  # 황금색
            QColor(211, 84, 0),    # 어두운 주황색
            QColor(41, 128, 185),  # 어두운 청색
            QColor(142, 68, 173),  # 어두운 보라색
            QColor(39, 174, 96),   # 어두운 녹색
            QColor(192, 57, 43),   # 어두운 빨강색
            QColor(127, 140, 141), # 은회색
        ]
        
        # 이미 사용 중인 색상들
        used_colors = list(self.partColors.values())
        
        # 사용 가능한 색상 필터링
        available_colors = [c for c in predefined_colors if c not in used_colors]
        
        if available_colors:
            # 사용 가능한 색상 중에서 무작위 선택
            return random.choice(available_colors)
        else:
            # 모든 색상이 사용 중이면 기존 색상에서 약간 변형
            base_color = random.choice(predefined_colors)
            hue_shift = random.randint(-20, 20)
            
            # HSL 색상 공간으로 변환
            h, s, l, a = base_color.getHslF()
            
            # 색조 변경 (0-1 범위에서)
            h = (h + hue_shift/360) % 1.0
            
            # 약간 다른 채도와 밝기
            s = min(1.0, max(0.5, s + random.uniform(-0.1, 0.1)))
            l = min(0.8, max(0.3, l + random.uniform(-0.1, 0.1)))
            
            # 새 색상 생성
            new_color = QColor()
            new_color.setHslF(h, s, l, a)
            return new_color
    
    def updatePartOrder(self):
        """파트 순서 업데이트 (드래그 앤 드롭 이후)"""
        # 현재 리스트의 순서에서 NamePart 이름 추출
        new_order = []
        for i in range(self.partsList.count()):
            item = self.partsList.item(i)
            widget = self.partsList.itemWidget(item)
            if widget:
                part = widget.getNamePart()
                new_order.append(part.get_name())
        
        # 새 순서 적용
        if new_order:
            self.configObj.reorder_parts(new_order)
            self.updatePreview()
    
    def updatePreview(self):
        """이름 미리보기 업데이트"""
        # 각 부분의 값 가져와서 조합
        preview_parts = []
        part_colors = []
        
        for i in range(self.partsList.count()):
            item = self.partsList.item(i)
            widget = self.partsList.itemWidget(item)
            if widget:
                value = widget.getValue()
                if value:
                    preview_parts.append(value)
                    part_colors.append(widget.getColor())
        
        # 미리보기 이름 업데이트 (구분 문자 사용)
        self.previewName = self.filteringChar.join(preview_parts)
        
        # 색상이 적용된 HTML 문자열 생성
        if self.previewName:
            html_parts = []
            
            # 구분 문자로 분리된 각 파트에 색상 적용
            parts = self.previewName.split(self.filteringChar)
            
            for i, part in enumerate(parts):
                if i < len(part_colors):
                    color = part_colors[i]
                    html_parts.append(f'<span style="color:{color.name()};">{part}</span>')
                else:
                    html_parts.append(part)
            
            # 구분 문자를 회색으로 표시
            separator_html = f'<span style="color:#999999;">{self.filteringChar}</span>'
            
            # HTML로 조합하여 미리보기 레이블에 설정
            preview_html = separator_html.join(html_parts)
            self.previewLabel.setText(preview_html)
        else:
            self.previewLabel.setText("")
        
        # Rich Text 형식 사용 설정
        self.previewLabel.setTextFormat(Qt.RichText)
    
    def onPartItemSelected(self, item):
        """NamePart 아이템 선택 시 처리"""
        widget = self.partsList.itemWidget(item)
        if widget:
            part = widget.getNamePart()
            self.loadPartDetails(part)
    
    def loadPartDetails(self, part: NamePart):
        """선택한 NamePart의 세부 정보 로드"""
        # 이름 설정
        self.partNameEdit.setText(part.get_name())
        
        # 타입 선택
        type_index = self.partTypeCombo.findText(part.get_type().name)
        if type_index >= 0:
            self.partTypeCombo.setCurrentIndex(type_index)
        
        # Direction 체크박스 상태 설정
        self.directionCheckBox.setChecked(part.is_direction())
        
        # 필수 부분 보호
        is_required = part.get_name() in self.configObj.required_parts
        self.partNameEdit.setEnabled(not is_required)
        
        # RealName과 Index는 타입 변경 비활성화
        if part.get_name() in ["RealName", "Index"]:
            self.partTypeCombo.setEnabled(False)
        else:
            self.partTypeCombo.setEnabled(True)
        
        # 값 테이블 업데이트
        self.updateValuesTable(part)
        
        # UI 상태 업데이트
        self.updatePartTypeUI()
    
    def updateValuesTable(self, part: NamePart):
        """값 테이블 업데이트"""
        self.valuesTable.setRowCount(0)
        
        # RealName과 Index는 사전 정의 값이 없음
        if part.is_realname() or part.is_index():
            return
        
        values = part.get_predefined_values()
        descriptions = part.get_descriptions()
        
        # 테이블에 값과 설명 추가
        for i, value in enumerate(values):
            self.valuesTable.insertRow(i)
            self.valuesTable.setItem(i, 0, QTableWidgetItem(value))
            
            # 설명이 있으면 설정
            description = ""
            if i < len(descriptions):
                description = descriptions[i]
            
            self.valuesTable.setItem(i, 1, QTableWidgetItem(description))
    
    def updatePartTypeUI(self):
        """NamePart 타입에 따라 UI 상태 업데이트"""
        current_type = self.partTypeCombo.currentText()
        
        # RealName과 Index 타입은 값 편집 비활성화
        is_edit_enabled = current_type not in ["REALNAME", "INDEX"]
        
        self.valuesTable.setEnabled(is_edit_enabled)
        self.addValueButton.setEnabled(is_edit_enabled)
        self.removeValueButton.setEnabled(is_edit_enabled)
    
    def addValue(self):
        """값 추가"""
        # 현재 선택된 아이템
        selected_items = self.partsList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "경고", "먼저 NamePart를 선택하세요.")
            return
        
        selected_item = selected_items[0]
        widget = self.partsList.itemWidget(selected_item)
        part = widget.getNamePart()
        
        # 새 행 추가
        row_count = self.valuesTable.rowCount()
        self.valuesTable.insertRow(row_count)
        
        # 기본값 설정
        new_value = f"Value{row_count + 1}"
        new_desc = f"Description{row_count + 1}"
        
        self.valuesTable.setItem(row_count, 0, QTableWidgetItem(new_value))
        self.valuesTable.setItem(row_count, 1, QTableWidgetItem(new_desc))
    
    def removeValue(self):
        """값 삭제"""
        selected_rows = self.valuesTable.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "경고", "삭제할 값을 선택하세요.")
            return
        
        # 현재 선택된 행
        row = selected_rows[0].row()
        
        # 값이 하나 이상 남아있는지 확인
        if self.valuesTable.rowCount() <= 1:
            QMessageBox.warning(self, "경고", "최소 하나의 값이 필요합니다.")
            return
        
        # 행 삭제
        self.valuesTable.removeRow(row)
    
    def updatePaddingNum(self, value):
        """패딩 자릿수 업데이트"""
        self.configObj.set_padding_num(value)
        self.updatePreview()
    
    def applyChanges(self):
        """변경 사항 적용"""
        # 선택된 항목 확인
        selected_items = self.partsList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "경고", "변경할 NamePart를 선택하세요.")
            return
        
        selected_item = selected_items[0]
        widget = self.partsList.itemWidget(selected_item)
        part = widget.getNamePart()
        old_name = part.get_name()
        
        try:
            # 타입 변경
            new_type_str = self.partTypeCombo.currentText()
            new_type = NamePartType[new_type_str]
            
            if new_type != part.get_type():
                self.configObj.set_part_type(old_name, new_type)
            
            # Direction 설정 변경
            part_obj = self.configObj.get_part(old_name)
            if part_obj:
                # is_direction 값이 변경되었는지 확인
                is_direction = self.directionCheckBox.isChecked()
                if is_direction != part_obj.is_direction():
                    # NamePart 객체의 _isDirection 속성 직접 설정
                    part_obj._isDirection = is_direction
            
            # 이름 변경 - 필수 부분이 아닌 경우만
            new_name = self.partNameEdit.text()
            if new_name and new_name != old_name and old_name not in self.configObj.required_parts:
                # 이름이 변경되었는지 확인
                if self.configObj.get_part(new_name):
                    QMessageBox.warning(self, "경고", f"'{new_name}' NamePart가 이미 존재합니다.")
                    return
                
                # 직접 NamePart 객체의 이름 변경
                part_obj = self.configObj.get_part(old_name)
                if part_obj:
                    # NamePart 이름 변경
                    part_obj.set_name(new_name)
                    
                    # 순서 목록에서도 이름 업데이트
                    part_order = self.configObj.get_part_order()
                    if old_name in part_order:
                        idx = part_order.index(old_name)
                        part_order[idx] = new_name
                        self.configObj._update_part_order()
            
            # 값 및 설명 변경 (RealName, Index 타입이 아닌 경우)
            current_name = new_name if new_name and new_name != old_name and old_name not in self.configObj.required_parts else old_name
            current_part = self.configObj.get_part(current_name)
            
            if not current_part.is_realname() and not current_part.is_index():
                values = []
                descriptions = []
                
                for row in range(self.valuesTable.rowCount()):
                    value_item = self.valuesTable.item(row, 0)
                    desc_item = self.valuesTable.item(row, 1)
                    
                    if value_item and value_item.text():
                        values.append(value_item.text())
                        descriptions.append(desc_item.text() if desc_item else "")
                
                # 값 설정
                if values:
                    current_part.set_predefined_values(values, descriptions)
            
            # UI 업데이트
            self.updateUI()
            
            QMessageBox.information(self, "알림", "변경 사항이 적용되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"변경 적용 중 오류 발생: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = NameConfigToolUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
