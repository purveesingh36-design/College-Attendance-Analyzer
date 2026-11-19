import os
import pandas as pd
import matplotlib.pyplot as plt

def load_and_validate_data(file_path):
    """Loads the CSV file and validates rows (Classes Attended <= Classes Held)."""
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return None
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

    # Check for required columns
    required_cols = {'Name', 'Subject', 'Classes_Held', 'Classes_Attended'}
    if not required_cols.issubset(df.columns):
        print(f"Error: CSV must contain the following columns: {required_cols}")
        return None

    # Validate rows: Attended cannot exceed Held
    valid_rows = []
    for index, row in df.iterrows():
        if row['Classes_Attended'] > row['Classes_Held']:
            print(f"Row {index + 1} invalid: attended ({row['Classes_Attended']}) cannot exceed held ({row['Classes_Held']}). Row skipped.")
        else:
            valid_rows.append(row)
            
    if not valid_rows:
        print("No valid rows found in the CSV.")
        return None

    valid_df = pd.DataFrame(valid_rows)
    # Calculate percentage column
    valid_df['Percentage'] = (valid_df['Classes_Attended'] / valid_df['Classes_Held']) * 100
    return valid_df

def main():
    file_path = "attendance.csv"
    
    # Optional: Automatically create a sample attendance.csv if it doesn't exist for testing
    if not os.path.exists(file_path):
        sample_data = """Name,Subject,Classes_Held,Classes_Attended
Aman,Python,40,36
Riya,Python,40,28
Karan,Python,40,30
Aman,Maths,50,45"""
        with open(file_path, "w") as f:
            f.write(sample_data)

    df = load_and_validate_data(file_path)
    if df is None:
        return

    while True:
        print("\n--- College Attendance Analyzer Menu ---")
        print("1. View Overall Percentage (Menu Option 1)")
        print("2. View Shortage List (< 75% Attendance) (Menu Option 2)")
        print("3. View Subject-wise Average & Charts (Menu Option 3)")
        print("4. Exit")
        
        choice = input("Enter your menu option (1-4): ").strip()
        
        if choice == '1':
            print("\n--- Student Attendance Percentages ---")
            result_str = " | ".join([f"{row['Name']}: {row['Percentage']:.2f}%" for _, row in df.iterrows()])
            print(result_str)
            
        elif choice == '2':
            print("\n--- Shortage List (< 75%) ---")
            shortage_df = df[df['Percentage'] < 75.0]
            if shortage_df.empty:
                print("No student below 75%.")
                # Show an eligible student example if present
                for _, row in df.iterrows():
                    print(f"{row['Name']} ({row['Percentage']:.2f}%) is eligible.")
                    break
            else:
                for _, row in shortage_df.iterrows():
                    print(f"{row['Name']} - {row['Percentage']:.2f}% (Shortage)")
                    
        elif choice == '3':
            print("\n--- Subject-wise Average ---")
            subject_avg = df.groupby('Subject')['Percentage'].mean()
            for subj, avg in subject_avg.items():
                print(f"{subj}: {avg:.2f}%")
            
            # Plotting Matplotlib Charts (Requirement: at least two charts - Bar and Pie)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Bar Chart: Subject-wise Average Percentage
            subject_avg.plot(kind='bar', ax=ax1, color='skyblue', edgecolor='black')
            ax1.set_title("Subject-wise Average Attendance")
            ax1.set_ylabel("Percentage (%)")
            ax1.set_ylim(0, 100)
            ax1.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Pie Chart: Attendance distribution or student percentage share
            ax2.pie(df['Percentage'], labels=df['Name'] + " (" + df['Subject'] + ")", autopct='%1.1f%%', startangle=140)
            ax2.set_title("Student Attendance Distribution")
            
            plt.tight_layout()
            plt.show()
            
        elif choice == '4':
            print("Exiting Attendance Analyzer. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 4.")

if __name__ == "__main__":
    main()