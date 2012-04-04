var kCellHeight=0.25;
var kCellWidth=0.25;


function Cell(row, column) {
    this.row = row;
    this.column = column;
};


function canvasOnClick(e) {
    var cell = getCursorPosition(e);

    // the rest of this is just gameplay logic
    for (var i = 0; i < gNumPieces; i++) {
	if ((gPieces[i].row == cell.row) && 
	    (gPieces[i].column == cell.column)) {
	    clickOnPiece(i);
	    return;
	}
    }
    clickOnEmptyCell(cell);
};

function getCursorPosition(e) {
    var x;
    var y;
    if (e.pageX != undefined && e.pageY != undefined) {
    	x = e.pageX;
    	y = e.pageY;
    }
    else {
    	x = e.clientX + document.body.scrollLeft +
    			document.documentElement.scrollLeft;
    	y = e.clientY + document.body.scrollTop +
    			document.documentElement.scrollTop;
    };
    x -= canvas.offsetLeft;
    y -= canvas.offsetTop;
    
    var cell = new Cell(Math.floor(y/kCellHeight), Math.floor(x/kCellWidth));
    //var cell = new Cell(y/kCellHeight, x/kCellWidth);
    alert("X: "+ cell.column + " width: " +kCellWidth );
    alert("Y: "+ cell.row + " height: " + kCellHeight );
    
    return cell;
    

};




