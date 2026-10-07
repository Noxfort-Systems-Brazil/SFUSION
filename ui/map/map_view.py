import logging
from PySide6.QtCore import Qt, Signal, Slot, QRectF, QPoint
from PySide6.QtGui import QPainter, QTransform
from PySide6.QtWidgets import (
    QGraphicsView, 
    QGraphicsScene, 
    QGraphicsItem, 
    QWidget
)


class MapView(QGraphicsView):
    """
    Specialized map view.
    
    Responsibilities:
    - Render scene (QGraphicsScene) with white background.
    - Process Pan (drag) and Zoom (scroll).
    - Detect clicks on items (nodes/edges) or empty space.
    - Emit signals (e.g. nodeClicked) to MapController.
    """
    
    # Signals for MapController
    nodeClicked = Signal(str)
    edgeClicked = Signal(str)
    
    # Empty space click signal does not take arguments
    emptySpaceClicked = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self._setup_view_settings()

        self._is_panning = False
        self._last_pan_point = None

        logging.info("MapView (View) initialized.")

    def _setup_view_settings(self):
        """Configure rendering and interaction settings."""
        self.setRenderHint(QPainter.Antialiasing) 
        self.scene.setBackgroundBrush(Qt.white) 

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

    # --- Public Methods (Called by Renderer) ---

    @Slot()
    def fit_map_in_view(self):
        """
        Fit the whole map inside the view.
        """
        try:
            rect = self.scene.itemsBoundingRect()
            if rect.isValid():
                rect.adjust(-rect.width() * 0.05, 
                            -rect.height() * 0.05,
                            rect.width() * 0.05, 
                            rect.height() * 0.05)
                
                self.fitInView(rect, Qt.KeepAspectRatio)
                logging.info(f"MapView: Zoom adjusted to map. (Rect: {rect})")
        except Exception as e:
            logging.error(f"MapView: Error adjusting zoom: {e}")

    @Slot(float, float)
    def set_zoom_limits(self, min_factor: float, max_factor: float):
        """Define minimum and maximum zoom limits."""
        logging.info(f"MapView: Zoom limits defined (Min: {min_factor}, Max: {max_factor})")

    # --- Interaction Events (Pan/Zoom/Click) ---

    def wheelEvent(self, event):
        """Handle mouse wheel scroll (Zoom)."""
        zoom_factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        """Handle mouse press (Start Pan or Click)."""
        
        if event.button() == Qt.MiddleButton:
            self._is_panning = True
            self._last_pan_point = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return

        if event.button() == Qt.LeftButton:
            self._on_scene_clicked(event.pos())
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse movement (Pan)."""
        if self._is_panning:
            delta = event.pos() - self._last_pan_point
            self._last_pan_point = event.pos()
            
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )
            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release (End Pan)."""
        if event.button() == Qt.MiddleButton:
            self._is_panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
            
        super().mouseReleaseEvent(event)

    # --- Click Logic ---

    @Slot(QPoint)
    def _on_scene_clicked(self, pos: QPoint):
        """
        Process a left click on the scene.
        Check if an item was clicked and emit the corresponding signal.
        """
        scene_pos = self.mapToScene(pos)
        item = self.itemAt(pos)

        if item:
            item_type = item.data(0)
            item_id = item.data(1) 

            if item_type == "node":
                self.nodeClicked.emit(item_id)
            elif item_type == "edge":
                self.edgeClicked.emit(item_id)
            
        else:
            # Signal emission matches definition (no args)
            self.emptySpaceClicked.emit()