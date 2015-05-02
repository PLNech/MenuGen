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
    [].forEach.call(cols, function (col) {
        col.classList.remove('over');
    });
    this.style.opacity = '1';
}

var counter = 0;

function handleDragEnter(e) {
    console.log("enter : " + counter);
    if (e.preventDefault) {
    e.preventDefault();
  }
    // this / e.target is the current hover target.
    counter++;

    this.classList.add('over');
}

function handleDragLeave(e) {
    console.log("leave : " + counter);
    counter--;
    if (counter === 0) {
        console.log(counter);
        this.classList.remove('over');  // this / e.target is previous target element.
    }
}


var cols = document.querySelectorAll('#planning .slot');
[].forEach.call(cols, function(col) {
    col.addEventListener('dragstart', handleDragStart, false);
    col.addEventListener('dragenter', handleDragEnter, false);
    col.addEventListener('dragover', handleDragOver, false);
    col.addEventListener('dragleave', handleDragLeave, false);
    col.addEventListener('drop', handleDrop, false);
    col.addEventListener('dragend', handleDragEnd, false);
});