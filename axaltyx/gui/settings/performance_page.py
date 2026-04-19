from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QComboBox, QCheckBox, QLabel, QHBoxLayout, QSpinBox
from axaltyx.core.managers import I18nManager, ConfigManager


class PerformancePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.config = ConfigManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # 内存设置
        memory_group = QGroupBox(self.i18n.t("settings.performance.memory"))
        memory_layout = QVBoxLayout()

        # 内存限制
        memory_limit_layout = QHBoxLayout()
        memory_limit_layout.addWidget(QLabel(self.i18n.t("settings.performance.memory_limit")))
        self.memory_limit_spinbox = QSpinBox()
        self.memory_limit_spinbox.setRange(1, 16)
        self.memory_limit_spinbox.setSuffix(" GB")
        memory_limit_layout.addWidget(self.memory_limit_spinbox)
        memory_layout.addLayout(memory_limit_layout)

        # 缓存大小
        cache_size_layout = QHBoxLayout()
        cache_size_layout.addWidget(QLabel(self.i18n.t("settings.performance.cache_size")))
        self.cache_size_spinbox = QSpinBox()
        self.cache_size_spinbox.setRange(100, 2000)
        self.cache_size_spinbox.setSuffix(" MB")
        cache_size_layout.addWidget(self.cache_size_spinbox)
        memory_layout.addLayout(cache_size_layout)

        memory_group.setLayout(memory_layout)
        layout.addWidget(memory_group)

        # 线程设置
        thread_group = QGroupBox(self.i18n.t("settings.performance.thread"))
        thread_layout = QVBoxLayout()

        # 线程数
        thread_count_layout = QHBoxLayout()
        thread_count_layout.addWidget(QLabel(self.i18n.t("settings.performance.thread_count")))
        self.thread_count_spinbox = QSpinBox()
        self.thread_count_spinbox.setRange(1, 8)
        thread_count_layout.addWidget(self.thread_count_spinbox)
        thread_layout.addLayout(thread_count_layout)

        # 并行处理
        self.parallel_processing_checkbox = QCheckBox(self.i18n.t("settings.performance.parallel_processing"))
        thread_layout.addWidget(self.parallel_processing_checkbox)

        thread_group.setLayout(thread_layout)
        layout.addWidget(thread_group)

        # 数据处理设置
        processing_group = QGroupBox(self.i18n.t("settings.performance.processing"))
        processing_layout = QVBoxLayout()

        # 数据块大小
        block_size_layout = QHBoxLayout()
        block_size_layout.addWidget(QLabel(self.i18n.t("settings.performance.block_size")))
        self.block_size_combo = QComboBox()
        self.block_size_combo.addItems(["1000", "5000", "10000", "50000"])
        block_size_layout.addWidget(self.block_size_combo)
        processing_layout.addLayout(block_size_layout)

        # 启用数据压缩
        self.compression_checkbox = QCheckBox(self.i18n.t("settings.performance.compression"))
        processing_layout.addWidget(self.compression_checkbox)

        # 启用数据预加载
        self.preload_checkbox = QCheckBox(self.i18n.t("settings.performance.preload"))
        processing_layout.addWidget(self.preload_checkbox)

        processing_group.setLayout(processing_layout)
        layout.addWidget(processing_group)

        # 加载设置
        self._load_settings()

        layout.addStretch()
        self.setLayout(layout)

    def _load_settings(self):
        # 加载内存设置
        self.memory_limit_spinbox.setValue(self.config.get("performance", "memory_limit", 4))
        self.cache_size_spinbox.setValue(self.config.get("performance", "cache_size", 500))

        # 加载线程设置
        self.thread_count_spinbox.setValue(self.config.get("performance", "thread_count", 4))
        self.parallel_processing_checkbox.setChecked(self.config.get("performance", "parallel_processing", True))

        # 加载数据处理设置
        block_size = self.config.get("performance", "block_size", "10000")
        self.block_size_combo.setCurrentText(block_size)
        self.compression_checkbox.setChecked(self.config.get("performance", "compression", False))
        self.preload_checkbox.setChecked(self.config.get("performance", "preload", True))

    def save_settings(self):
        # 保存内存设置
        self.config.set("performance", "memory_limit", self.memory_limit_spinbox.value())
        self.config.set("performance", "cache_size", self.cache_size_spinbox.value())

        # 保存线程设置
        self.config.set("performance", "thread_count", self.thread_count_spinbox.value())
        self.config.set("performance", "parallel_processing", self.parallel_processing_checkbox.isChecked())

        # 保存数据处理设置
        self.config.set("performance", "block_size", self.block_size_combo.currentText())
        self.config.set("performance", "compression", self.compression_checkbox.isChecked())
        self.config.set("performance", "preload", self.preload_checkbox.isChecked())
