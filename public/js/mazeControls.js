/* This script lets the user control various aspects of the maze being drawn. */
var maze = new Maze(5, 5);

window.onload = function () {
    var canvas = document.createElement("canvas"),
        context = canvas.getContext('2d'),
        gradient = context.createLinearGradient(0, 0, 401, 401);

    canvas.setAttribute("width", "401");
    canvas.setAttribute("height", "401");

    document.getElementById("mazeHolder").insertAdjacentElement("afterBegin",
                                                                canvas);
    gradient.addColorStop(0, "#000044");
    gradient.addColorStop(0.8, "#3366FF");

    function drawMaze(width, height) {
        context.fillStyle = "#FFFFFF";
        context.fillRect(0, 0, 401, 401);


        maze = new Maze(width, height);
        console.log(maze)
        var step = 400 / Math.max(width, height);
        if(maze.flag)
        {
            maze.draw(canvas, step, {wall : gradient, background : "#FFBB88"})
        }
        else
        {
            drawMaze(width, height)
        }
        context.beginPath();
        context.arc(0, 0, 10, 0, Math.PI*2);
        context.fillStyle = "#0095DD";
        context.fill();
        context.closePath();
    }

    drawMaze(5, 5);
    
    // Controls:
    var widthInput = document.getElementById("width"),
        heightInput = document.getElementById("height"),
        drawButton = document.getElementById("draw"),
        solveButton = document.getElementById("solve");

    drawButton.onclick = function () {
        drawMaze(widthInput.value, heightInput.value);
        console.log(maze.cells)
    };

    solveButton.onclick = function () {
        var s = maze.drawSolution(canvas);
    };
};