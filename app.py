from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from main import TASKS, run_workflow
import traceback

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', tasks=TASKS)

@app.route('/execute_task', methods=['POST'])
def execute_task():
    try:
        task_key = request.form['task_key']
        if task_key not in TASKS:
            return jsonify({
                'success': False,
                'error': 'Invalid task key'
            })

        # Run workflow with fresh state
        result = run_workflow(TASKS[task_key])
        
        if not result or not isinstance(result, dict):
            return jsonify({
                'success': False,
                'error': 'Invalid result format'
            })

        if 'final_summary' not in result:
            return jsonify({
                'success': False,
                'error': 'No summary generated'
            })

        # Format the summary for better display
        formatted_summary = result['final_summary'].strip()
        if not formatted_summary:
            return jsonify({
                'success': False,
                'error': 'Empty summary generated'
            })
        
        return jsonify({
            'success': True,
            'summary': formatted_summary
        })

    except Exception as e:
        # Get detailed error information
        error_details = traceback.format_exc()
        print(f"Error details: {error_details}")
        
        return jsonify({
            'success': False,
            'error': f'Task execution failed: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True) 