from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from main import TASKS, run_workflow
import traceback
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', tasks=TASKS)

@app.route('/create_task', methods=['GET'])
def create_task():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a task creator for a business management system. Create a complex business task that requires coordination between personnel, logistics, PR, intelligence, and operations teams. The task should be challenging but achievable."},
                {"role": "user", "content": "Generate a new business task."}
            ]
        )
        new_task = response.choices[0].message.content.strip()
        return jsonify({"success": True, "task": new_task})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/execute_task', methods=['POST'])
def execute_task():
    try:
        task_key = request.form['task_key']
        task_text = request.form['task_text']

        # Handle both predefined and AI-generated tasks
        if task_key == 'ai_generated':
            task = task_text
        elif task_key in TASKS:
            task = TASKS[task_key]
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid task key'
            })

        # Run workflow with fresh state
        result = run_workflow(task)
        
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