function handleDragStart(e) {
    console.log("dragstart");
    this.style.opacity = '0.4';  // this / e.target is the source node.

    dragSrcEl = this;

    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}

function handleDragOver(e) {
    console.log("dragover");
  if (e.preventDefault) {
    e.preventDefault(); // Necessary. Allows us to drop.
  }

  e.dataTransfer.dropEffect = 'move';

  return false;
}

function handleDrop(e) {
  // this / e.target is current target element.
    console.log("drop");
  if (e.stopPropagation) {
    e.stopPropagation(); // stops the browser from redirecting.
  }

    // Don't do anything if dropping the same column we're dragging.
  if (dragSrcEl != this) {
    // Set the source column's HTML to the HTML of the column we dropped on.
    dragSrcEl.innerHTML = this.innerHTML;
    this.innerHTML = e.dataTransfer.getData('text/html');
  }

  return false;
}

function handleDragEnd(e) {
    // this/e.target is the source node.
    console.log("dragend");
    [].forEach.call(cols, function (col) {
        col.classList.remove('over');
    });
    this.style.opacity = '1';
}
