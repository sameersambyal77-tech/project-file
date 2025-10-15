"""
Sorting Algorithm Visualizer
Visualizes Insertion Sort, Selection Sort, Bubble Sort, Merge Sort, and Quick Sort
with time complexity comparison and step-by-step animation.
"""

import tkinter as tk
from tkinter import ttk
import random
import time

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Color scheme
        self.colors = {
            'default': '#3498db',
            'comparing': '#e74c3c',
            'sorted': '#2ecc71',
            'pivot': '#f39c12',
            'current': '#9b59b6'
        }
        
        # Algorithm data
        self.array = []
        self.array_size = 50
        self.speed = 50  # milliseconds
        self.sorting = False
        self.stats = {'comparisons': 0, 'swaps': 0, 'time': 0}
        
        # Time complexity information
        self.complexity_info = {
            'Bubble Sort': {'best': 'O(n)', 'average': 'O(n²)', 'worst': 'O(n²)', 'space': 'O(1)'},
            'Selection Sort': {'best': 'O(n²)', 'average': 'O(n²)', 'worst': 'O(n²)', 'space': 'O(1)'},
            'Insertion Sort': {'best': 'O(n)', 'average': 'O(n²)', 'worst': 'O(n²)', 'space': 'O(1)'},
            'Merge Sort': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n log n)', 'space': 'O(n)'},
            'Quick Sort': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n²)', 'space': 'O(log n)'}
        }
        
        self.setup_ui()
        self.generate_array()
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="Sorting Algorithm Visualizer", 
                              font=("Arial", 24, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=15)
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg="#ecf0f1", height=120)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Algorithm selection
        tk.Label(control_frame, text="Algorithm:", font=("Arial", 12), 
                bg="#ecf0f1").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        algorithm_menu = ttk.Combobox(control_frame, textvariable=self.algorithm_var,
                                     values=['Bubble Sort', 'Selection Sort', 'Insertion Sort', 
                                           'Merge Sort', 'Quick Sort'],
                                     state="readonly", width=15, font=("Arial", 11))
        algorithm_menu.grid(row=0, column=1, padx=10, pady=5)
        algorithm_menu.bind('<<ComboboxSelected>>', self.update_complexity_display)
        
        # Speed control
        tk.Label(control_frame, text="Speed:", font=("Arial", 12), 
                bg="#ecf0f1").grid(row=0, column=2, padx=10, pady=5)
        
        speed_scale = tk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                              command=self.update_speed, length=150, bg="#ecf0f1")
        speed_scale.set(50)
        speed_scale.grid(row=0, column=3, padx=10, pady=5)
        
        # Array size control
        tk.Label(control_frame, text="Array Size:", font=("Arial", 12), 
                bg="#ecf0f1").grid(row=0, column=4, padx=10, pady=5)
        
        size_scale = tk.Scale(control_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                             command=self.update_size, length=150, bg="#ecf0f1")
        size_scale.set(50)
        size_scale.grid(row=0, column=5, padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg="#ecf0f1")
        button_frame.grid(row=1, column=0, columnspan=6, pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start Sorting", 
                                      command=self.start_sorting, font=("Arial", 12, "bold"),
                                      bg="#27ae60", fg="white", padx=20, pady=5)
        self.start_button.grid(row=0, column=0, padx=10)
        
        self.reset_button = tk.Button(button_frame, text="Generate New Array", 
                                      command=self.generate_array, font=("Arial", 12),
                                      bg="#3498db", fg="white", padx=20, pady=5)
        self.reset_button.grid(row=0, column=1, padx=10)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg="#ecf0f1", height=80)
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Comparisons: 0 | Swaps: 0 | Time: 0.00s", 
                                   font=("Arial", 14), bg="#ecf0f1", fg="#2c3e50")
        self.stats_label.pack(pady=10)
        
        # Complexity info frame
        complexity_frame = tk.Frame(self.root, bg="#ecf0f1", height=60)
        complexity_frame.pack(fill=tk.X, pady=5)
        
        self.complexity_label = tk.Label(complexity_frame, text="", 
                                        font=("Arial", 11), bg="#ecf0f1", fg="#34495e")
        self.complexity_label.pack(pady=5)
        self.update_complexity_display()
        
        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, bg="white", height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def update_complexity_display(self, event=None):
        algo = self.algorithm_var.get()
        info = self.complexity_info[algo]
        text = f"Time Complexity - Best: {info['best']} | Average: {info['average']} | Worst: {info['worst']} | Space: {info['space']}"
        self.complexity_label.config(text=text)
    
    def update_speed(self, val):
        self.speed = 101 - int(val)  # Invert so higher value = faster
    
    def update_size(self, val):
        if not self.sorting:
            self.array_size = int(val)
            self.generate_array()
    
    def generate_array(self):
        if not self.sorting:
            self.array = [random.randint(10, 400) for _ in range(self.array_size)]
            self.stats = {'comparisons': 0, 'swaps': 0, 'time': 0}
            self.update_stats()
            self.draw_array()
    
    def draw_array(self, color_array=None):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = 400
        
        if canvas_width <= 1:
            canvas_width = 960
        
        bar_width = canvas_width / len(self.array)
        
        for i, height in enumerate(self.array):
            x0 = i * bar_width
            y0 = canvas_height - height
            x1 = (i + 1) * bar_width
            y1 = canvas_height
            
            color = self.colors['default']
            if color_array and i < len(color_array):
                color = color_array[i]
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
        
        self.root.update_idletasks()
    
    def update_stats(self):
        self.stats_label.config(
            text=f"Comparisons: {self.stats['comparisons']} | "
                 f"Swaps: {self.stats['swaps']} | "
                 f"Time: {self.stats['time']:.2f}s"
        )
    
    def start_sorting(self):
        if not self.sorting:
            self.sorting = True
            self.start_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.DISABLED)
            
            self.stats = {'comparisons': 0, 'swaps': 0, 'time': 0}
            start_time = time.time()
            
            algorithm = self.algorithm_var.get()
            
            if algorithm == 'Bubble Sort':
                self.bubble_sort()
            elif algorithm == 'Selection Sort':
                self.selection_sort()
            elif algorithm == 'Insertion Sort':
                self.insertion_sort()
            elif algorithm == 'Merge Sort':
                self.merge_sort_wrapper()
            elif algorithm == 'Quick Sort':
                self.quick_sort_wrapper()
            
            self.stats['time'] = time.time() - start_time
            self.update_stats()
            
            # Color entire array green
            color_array = [self.colors['sorted'] for _ in range(len(self.array))]
            self.draw_array(color_array)
            
            self.sorting = False
            self.start_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
    
    # Sorting Algorithms
    
    def bubble_sort(self):
        n = len(self.array)
        for i in range(n):
            swapped = False
            for j in range(n - i - 1):
                self.stats['comparisons'] += 1
                self.update_stats()
                
                color_array = [self.colors['default']] * len(self.array)
                color_array[j] = self.colors['comparing']
                color_array[j + 1] = self.colors['comparing']
                
                # Mark sorted elements
                for k in range(n - i, n):
                    color_array[k] = self.colors['sorted']
                
                self.draw_array(color_array)
                time.sleep(self.speed / 1000)
                
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.stats['swaps'] += 1
                    swapped = True
            
            if not swapped:
                break
    
    def selection_sort(self):
        n = len(self.array)
        for i in range(n):
            min_idx = i
            
            for j in range(i + 1, n):
                self.stats['comparisons'] += 1
                self.update_stats()
                
                color_array = [self.colors['default']] * len(self.array)
                color_array[min_idx] = self.colors['current']
                color_array[j] = self.colors['comparing']
                
                # Mark sorted elements
                for k in range(i):
                    color_array[k] = self.colors['sorted']
                
                self.draw_array(color_array)
                time.sleep(self.speed / 1000)
                
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                self.stats['swaps'] += 1
    
    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1
            
            while j >= 0:
                self.stats['comparisons'] += 1
                self.update_stats()
                
                color_array = [self.colors['default']] * len(self.array)
                color_array[i] = self.colors['current']
                color_array[j] = self.colors['comparing']
                
                # Mark sorted portion
                for k in range(i):
                    if color_array[k] == self.colors['default']:
                        color_array[k] = self.colors['sorted']
                
                self.draw_array(color_array)
                time.sleep(self.speed / 1000)
                
                if self.array[j] > key:
                    self.array[j + 1] = self.array[j]
                    self.stats['swaps'] += 1
                    j -= 1
                else:
                    break
            
            self.array[j + 1] = key
    
    def merge_sort_wrapper(self):
        self.merge_sort(0, len(self.array) - 1)
    
    def merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            
            self.merge_sort(left, mid)
            self.merge_sort(mid + 1, right)
            self.merge(left, mid, right)
    
    def merge(self, left, mid, right):
        left_part = self.array[left:mid + 1]
        right_part = self.array[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            self.stats['comparisons'] += 1
            self.update_stats()
            
            color_array = [self.colors['default']] * len(self.array)
            for idx in range(left, right + 1):
                color_array[idx] = self.colors['comparing']
            
            self.draw_array(color_array)
            time.sleep(self.speed / 1000)
            
            if left_part[i] <= right_part[j]:
                self.array[k] = left_part[i]
                i += 1
            else:
                self.array[k] = right_part[j]
                j += 1
            
            self.stats['swaps'] += 1
            k += 1
        
        while i < len(left_part):
            self.array[k] = left_part[i]
            i += 1
            k += 1
        
        while j < len(right_part):
            self.array[k] = right_part[j]
            j += 1
            k += 1
    
    def quick_sort_wrapper(self):
        self.quick_sort(0, len(self.array) - 1)
    
    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)
    
    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        
        for j in range(low, high):
            self.stats['comparisons'] += 1
            self.update_stats()
            
            color_array = [self.colors['default']] * len(self.array)
            color_array[high] = self.colors['pivot']
            color_array[j] = self.colors['comparing']
            if i >= 0:
                color_array[i] = self.colors['current']
            
            self.draw_array(color_array)
            time.sleep(self.speed / 1000)
            
            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                self.stats['swaps'] += 1
        
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        self.stats['swaps'] += 1
        
        return i + 1


def main():
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
