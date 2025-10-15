# Sorting-Based Projects

This repository contains two comprehensive sorting algorithm projects in Python.

## 🎯 Projects Overview

### 1. Sorting Visualizer (`sorting_visualizer.py`)
A beautiful graphical application that visualizes sorting algorithms in real-time.

**Features:**
- ✨ Real-time visualization with color-coded bars
- 🎨 Beautiful modern UI with Tkinter
- 📊 Five sorting algorithms:
  - Bubble Sort
  - Selection Sort
  - Insertion Sort
  - Merge Sort
  - Quick Sort
- ⚡ Adjustable speed control (1-100)
- 📏 Adjustable array size (10-100 elements)
- 📈 Live statistics: comparisons, swaps, and execution time
- 🧮 Time complexity display for each algorithm
- 🎯 Color coding:
  - Blue: Default/Unsorted
  - Red: Currently comparing
  - Green: Sorted
  - Orange: Pivot (Quick Sort)
  - Purple: Current element (Insertion Sort)

**Time Complexities:**
| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |

**How to Run:**
```bash
python sorting_visualizer.py
```

**Usage:**
1. Select a sorting algorithm from the dropdown
2. Adjust speed and array size using sliders
3. Click "Start Sorting" to begin visualization
4. Click "Generate New Array" to create a new random array
5. Watch the algorithm work step-by-step!

---

### 2. Student Ranker (`student_ranker.py`)
A console-based application that ranks students by marks using different sorting algorithms.

**Features:**
- 👨‍🎓 Add unlimited students with names and marks
- 🏆 Rank students using three sorting algorithms:
  - Insertion Sort
  - Selection Sort
  - Bubble Sort (Bonus)
- 📊 Detailed step-by-step sorting process
- 🔢 Track comparisons and swaps for each algorithm
- 🆚 Compare all algorithms side-by-side
- 🎯 Handle tied ranks correctly
- 📝 Sample data for quick testing
- 💾 Interactive menu-driven interface

**Features Highlight:**
- **Step-by-step visualization**: See exactly how each algorithm works
- **Statistics tracking**: Comparisons, swaps, and total operations
- **Rank handling**: Properly handles students with same marks
- **Algorithm comparison**: Compare efficiency of all three algorithms
- **Sample data**: Quick testing with pre-loaded student data

**How to Run:**
```bash
python student_ranker.py
```

**Menu Options:**
1. **Add Students** - Manually add student names and marks
2. **Rank using Insertion Sort** - Sort and display with detailed steps
3. **Rank using Selection Sort** - Sort and display with detailed steps
4. **Rank using Bubble Sort** - Sort and display with detailed steps
5. **Compare All Algorithms** - Run all algorithms and compare performance
6. **Display Current Students** - View all students in the system
7. **Clear All Students** - Remove all students
8. **Load Sample Data** - Load 10 pre-defined students for testing
9. **Exit** - Quit the program

**Sample Output:**
```
FINAL RANKINGS - Insertion Sort
======================================================================
Rank    Name                     Marks     
----------------------------------------------------------------------
#1      Alice Johnson            95.50     
#1      Eve Anderson             95.50     
#3      Jack Wilson              94.20     
#4      Charlie Brown            92.30     
#5      Grace Lee                91.00     

======================================================================
ALGORITHM STATISTICS
======================================================================
Total Comparisons: 23
Total Swaps: 15
Total Operations: 38
======================================================================
```

## 🛠️ Requirements

- Python 3.7 or higher
- tkinter (for sorting visualizer - usually comes with Python)

### Installing tkinter (if needed):

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
tkinter comes with Python from python.org

**Windows:**
tkinter comes with the official Python installer

## 🚀 Quick Start

1. Clone or download this repository
2. Ensure Python 3.7+ is installed
3. Run either program:
   ```bash
   # For visual sorting algorithm demonstration
   python sorting_visualizer.py
   
   # For student ranking system
   python student_ranker.py
   ```

## 📚 Educational Value

### Sorting Visualizer
- **Visual Learning**: See how algorithms work in real-time
- **Performance Comparison**: Compare different algorithms visually
- **Time Complexity**: Understand Big O notation through practical examples
- **Algorithm Behavior**: Observe best/worst case scenarios

### Student Ranker
- **Practical Application**: Real-world use case of sorting
- **Algorithm Analysis**: Compare efficiency through actual counts
- **Step-by-step Learning**: Understand each algorithm's logic
- **Data Structures**: Work with custom objects (Student class)

## 🎓 Learning Outcomes

After using these projects, you will understand:

1. **How different sorting algorithms work** - Visual and step-by-step explanations
2. **Time and space complexity** - Practical performance differences
3. **When to use which algorithm** - Best use cases for each sorting method
4. **Algorithm efficiency** - Comparison counts and swap operations
5. **Real-world applications** - Practical use of sorting in ranking systems

## 💡 Tips for Best Learning Experience

### For Sorting Visualizer:
- Start with a small array size (10-20) to see detailed steps
- Use slower speed to observe algorithm behavior
- Try the same algorithm multiple times with "Generate New Array"
- Compare fast algorithms (Merge/Quick) with slow ones (Bubble/Selection)

### For Student Ranker:
- Load sample data first to see how it works
- Try "Compare All Algorithms" to see efficiency differences
- Add students with same marks to understand rank handling
- Read the step-by-step output to understand algorithm logic

## 🔬 Experiment Ideas

1. **Sorting Visualizer:**
   - How does array size affect performance?
   - Which algorithm handles nearly-sorted data best?
   - What happens with reverse-sorted arrays?

2. **Student Ranker:**
   - How do algorithms compare with 5 vs 50 students?
   - What happens when all students have the same marks?
   - Which algorithm is most efficient for your data?

## 📝 Code Structure

### sorting_visualizer.py
- `SortingVisualizer` class: Main application
- Individual sorting methods with visualization
- Tkinter UI components
- Real-time statistics tracking

### student_ranker.py
- `Student` class: Student data model
- `StudentRanker` class: Sorting and ranking logic
- Interactive menu system
- Detailed algorithm step output

## 🤝 Contributing

Feel free to enhance these projects:
- Add more sorting algorithms (Heap Sort, Radix Sort, etc.)
- Improve UI/UX
- Add more statistics
- Create additional visualizations
- Add sound effects to the visualizer

## 📄 License

These projects are created for educational purposes. Feel free to use and modify for learning!

---

**Happy Sorting! 🎉**

Made with ❤️ for learning data structures and algorithms
