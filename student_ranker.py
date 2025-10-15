"""
Student Ranking System
Uses sorting algorithms (Insertion Sort & Selection Sort) to rank students by marks.
Displays the number of comparisons and swaps made during sorting.
"""

import sys
from typing import List, Tuple, Dict


class Student:
    """Represents a student with name and marks."""
    
    def __init__(self, name: str, marks: float):
        self.name = name
        self.marks = marks
        self.rank = 0
    
    def __repr__(self):
        return f"Student(name='{self.name}', marks={self.marks}, rank={self.rank})"
    
    def __str__(self):
        return f"{self.name}: {self.marks} marks (Rank #{self.rank})"


class StudentRanker:
    """Handles student ranking using different sorting algorithms."""
    
    def __init__(self):
        self.students: List[Student] = []
        self.stats: Dict[str, int] = {'comparisons': 0, 'swaps': 0}
    
    def add_student(self, name: str, marks: float):
        """Add a student to the list."""
        self.students.append(Student(name, marks))
    
    def reset_stats(self):
        """Reset comparison and swap counters."""
        self.stats = {'comparisons': 0, 'swaps': 0}
    
    def insertion_sort(self) -> Tuple[List[Student], Dict[str, int]]:
        """
        Sort students using Insertion Sort algorithm.
        Returns sorted list and statistics.
        """
        self.reset_stats()
        students_copy = [s for s in self.students]
        n = len(students_copy)
        
        print("\n" + "="*70)
        print("INSERTION SORT - Step by Step Process")
        print("="*70)
        
        for i in range(1, n):
            key = students_copy[i]
            j = i - 1
            
            print(f"\nStep {i}: Inserting {key.name} ({key.marks} marks)")
            
            # Compare and shift elements
            while j >= 0:
                self.stats['comparisons'] += 1
                
                if students_copy[j].marks < key.marks:  # Sort in descending order
                    students_copy[j + 1] = students_copy[j]
                    self.stats['swaps'] += 1
                    print(f"  → Shifting {students_copy[j].name} to position {j+2}")
                    j -= 1
                else:
                    break
            
            students_copy[j + 1] = key
            print(f"  → Placed {key.name} at position {j+2}")
            
            # Show current state
            print(f"  Current order: {', '.join([s.name for s in students_copy])}")
        
        # Assign ranks
        self._assign_ranks(students_copy)
        
        return students_copy, self.stats.copy()
    
    def selection_sort(self) -> Tuple[List[Student], Dict[str, int]]:
        """
        Sort students using Selection Sort algorithm.
        Returns sorted list and statistics.
        """
        self.reset_stats()
        students_copy = [s for s in self.students]
        n = len(students_copy)
        
        print("\n" + "="*70)
        print("SELECTION SORT - Step by Step Process")
        print("="*70)
        
        for i in range(n):
            max_idx = i
            
            print(f"\nStep {i+1}: Finding student with highest marks from position {i+1}")
            
            # Find the maximum element in remaining unsorted array
            for j in range(i + 1, n):
                self.stats['comparisons'] += 1
                
                if students_copy[j].marks > students_copy[max_idx].marks:
                    max_idx = j
                    print(f"  → Found higher marks: {students_copy[j].name} ({students_copy[j].marks})")
            
            # Swap if needed
            if max_idx != i:
                print(f"  → Swapping {students_copy[i].name} with {students_copy[max_idx].name}")
                students_copy[i], students_copy[max_idx] = students_copy[max_idx], students_copy[i]
                self.stats['swaps'] += 1
            else:
                print(f"  → {students_copy[i].name} is already in correct position")
            
            # Show current state
            print(f"  Current order: {', '.join([s.name for s in students_copy])}")
        
        # Assign ranks
        self._assign_ranks(students_copy)
        
        return students_copy, self.stats.copy()
    
    def bubble_sort(self) -> Tuple[List[Student], Dict[str, int]]:
        """
        Sort students using Bubble Sort algorithm (bonus).
        Returns sorted list and statistics.
        """
        self.reset_stats()
        students_copy = [s for s in self.students]
        n = len(students_copy)
        
        print("\n" + "="*70)
        print("BUBBLE SORT - Step by Step Process")
        print("="*70)
        
        for i in range(n):
            swapped = False
            print(f"\nPass {i+1}:")
            
            for j in range(n - i - 1):
                self.stats['comparisons'] += 1
                
                if students_copy[j].marks < students_copy[j + 1].marks:
                    print(f"  → Swapping {students_copy[j].name} ({students_copy[j].marks}) "
                          f"with {students_copy[j+1].name} ({students_copy[j+1].marks})")
                    students_copy[j], students_copy[j + 1] = students_copy[j + 1], students_copy[j]
                    self.stats['swaps'] += 1
                    swapped = True
            
            if not swapped:
                print("  → No swaps made, array is sorted!")
                break
            
            print(f"  Current order: {', '.join([s.name for s in students_copy])}")
        
        # Assign ranks
        self._assign_ranks(students_copy)
        
        return students_copy, self.stats.copy()
    
    def _assign_ranks(self, sorted_students: List[Student]):
        """Assign ranks to sorted students, handling ties."""
        if not sorted_students:
            return
        
        current_rank = 1
        sorted_students[0].rank = current_rank
        
        for i in range(1, len(sorted_students)):
            if sorted_students[i].marks == sorted_students[i-1].marks:
                # Same marks = same rank
                sorted_students[i].rank = sorted_students[i-1].rank
            else:
                current_rank = i + 1
                sorted_students[i].rank = current_rank
    
    def display_rankings(self, sorted_students: List[Student], stats: Dict[str, int], algorithm: str):
        """Display the final rankings with statistics."""
        print("\n" + "="*70)
        print(f"FINAL RANKINGS - {algorithm}")
        print("="*70)
        print(f"{'Rank':<8}{'Name':<25}{'Marks':<10}")
        print("-" * 70)
        
        for student in sorted_students:
            rank_str = f"#{student.rank}"
            print(f"{rank_str:<8}{student.name:<25}{student.marks:<10.2f}")
        
        print("\n" + "="*70)
        print("ALGORITHM STATISTICS")
        print("="*70)
        print(f"Total Comparisons: {stats['comparisons']}")
        print(f"Total Swaps: {stats['swaps']}")
        print(f"Total Operations: {stats['comparisons'] + stats['swaps']}")
        print("="*70 + "\n")


def print_menu():
    """Display the main menu."""
    print("\n" + "="*70)
    print("STUDENT RANKING SYSTEM")
    print("="*70)
    print("1. Add Students")
    print("2. Rank Students using Insertion Sort")
    print("3. Rank Students using Selection Sort")
    print("4. Rank Students using Bubble Sort (Bonus)")
    print("5. Compare All Algorithms")
    print("6. Display Current Students")
    print("7. Clear All Students")
    print("8. Load Sample Data")
    print("9. Exit")
    print("="*70)


def load_sample_data(ranker: StudentRanker):
    """Load sample student data for testing."""
    sample_students = [
        ("Alice Johnson", 95.5),
        ("Bob Smith", 87.0),
        ("Charlie Brown", 92.3),
        ("Diana Prince", 88.5),
        ("Eve Anderson", 95.5),  # Same as Alice (tie)
        ("Frank Miller", 78.0),
        ("Grace Lee", 91.0),
        ("Henry Davis", 85.5),
        ("Ivy Chen", 89.0),
        ("Jack Wilson", 94.2)
    ]
    
    ranker.students.clear()
    for name, marks in sample_students:
        ranker.add_student(name, marks)
    
    print(f"\n✓ Loaded {len(sample_students)} sample students successfully!")


def add_students_interactive(ranker: StudentRanker):
    """Interactive mode to add students."""
    print("\n--- Add Students ---")
    print("Enter student details (or 'done' to finish)")
    
    count = 0
    while True:
        name = input(f"\nStudent #{len(ranker.students) + 1} Name (or 'done'): ").strip()
        
        if name.lower() == 'done':
            break
        
        if not name:
            print("⚠ Name cannot be empty. Please try again.")
            continue
        
        try:
            marks = float(input(f"Marks for {name}: ").strip())
            
            if marks < 0 or marks > 100:
                print("⚠ Marks should be between 0 and 100. Please try again.")
                continue
            
            ranker.add_student(name, marks)
            count += 1
            print(f"✓ Added {name} with {marks} marks")
            
        except ValueError:
            print("⚠ Invalid marks. Please enter a number.")
    
    if count > 0:
        print(f"\n✓ Successfully added {count} student(s)!")


def display_students(ranker: StudentRanker):
    """Display all current students."""
    if not ranker.students:
        print("\n⚠ No students in the system. Please add students first.")
        return
    
    print("\n" + "="*70)
    print("CURRENT STUDENTS")
    print("="*70)
    print(f"{'#':<5}{'Name':<30}{'Marks':<10}")
    print("-" * 70)
    
    for i, student in enumerate(ranker.students, 1):
        print(f"{i:<5}{student.name:<30}{student.marks:<10.2f}")
    
    print("="*70)


def compare_algorithms(ranker: StudentRanker):
    """Compare all sorting algorithms."""
    if not ranker.students:
        print("\n⚠ No students in the system. Please add students first.")
        return
    
    print("\n" + "="*70)
    print("ALGORITHM COMPARISON")
    print("="*70)
    
    # Run all algorithms
    _, insertion_stats = ranker.insertion_sort()
    _, selection_stats = ranker.selection_sort()
    _, bubble_stats = ranker.bubble_sort()
    
    # Display comparison table
    print("\n" + "="*70)
    print("PERFORMANCE COMPARISON")
    print("="*70)
    print(f"{'Algorithm':<20}{'Comparisons':<15}{'Swaps':<15}{'Total Ops':<15}")
    print("-" * 70)
    
    print(f"{'Insertion Sort':<20}{insertion_stats['comparisons']:<15}"
          f"{insertion_stats['swaps']:<15}"
          f"{insertion_stats['comparisons'] + insertion_stats['swaps']:<15}")
    
    print(f"{'Selection Sort':<20}{selection_stats['comparisons']:<15}"
          f"{selection_stats['swaps']:<15}"
          f"{selection_stats['comparisons'] + selection_stats['swaps']:<15}")
    
    print(f"{'Bubble Sort':<20}{bubble_stats['comparisons']:<15}"
          f"{bubble_stats['swaps']:<15}"
          f"{bubble_stats['comparisons'] + bubble_stats['swaps']:<15}")
    
    print("="*70)
    
    # Determine the most efficient
    algorithms = [
        ('Insertion Sort', insertion_stats['comparisons'] + insertion_stats['swaps']),
        ('Selection Sort', selection_stats['comparisons'] + selection_stats['swaps']),
        ('Bubble Sort', bubble_stats['comparisons'] + bubble_stats['swaps'])
    ]
    
    most_efficient = min(algorithms, key=lambda x: x[1])
    print(f"\n🏆 Most Efficient: {most_efficient[0]} with {most_efficient[1]} total operations")
    print("="*70 + "\n")


def main():
    """Main function to run the student ranking system."""
    ranker = StudentRanker()
    
    print("\n" + "🎓" * 35)
    print("Welcome to the Student Ranking System!")
    print("🎓" * 35)
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-9): ").strip()
        
        if choice == '1':
            add_students_interactive(ranker)
        
        elif choice == '2':
            if not ranker.students:
                print("\n⚠ No students in the system. Please add students first.")
            else:
                sorted_students, stats = ranker.insertion_sort()
                ranker.display_rankings(sorted_students, stats, "Insertion Sort")
        
        elif choice == '3':
            if not ranker.students:
                print("\n⚠ No students in the system. Please add students first.")
            else:
                sorted_students, stats = ranker.selection_sort()
                ranker.display_rankings(sorted_students, stats, "Selection Sort")
        
        elif choice == '4':
            if not ranker.students:
                print("\n⚠ No students in the system. Please add students first.")
            else:
                sorted_students, stats = ranker.bubble_sort()
                ranker.display_rankings(sorted_students, stats, "Bubble Sort")
        
        elif choice == '5':
            compare_algorithms(ranker)
        
        elif choice == '6':
            display_students(ranker)
        
        elif choice == '7':
            ranker.students.clear()
            print("\n✓ All students cleared successfully!")
        
        elif choice == '8':
            load_sample_data(ranker)
        
        elif choice == '9':
            print("\n" + "="*70)
            print("Thank you for using the Student Ranking System!")
            print("Goodbye! 👋")
            print("="*70 + "\n")
            sys.exit(0)
        
        else:
            print("\n⚠ Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
