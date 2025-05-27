from flask import Blueprint, render_template, request, session, Response, jsonify
from services import DownloadFormat, ExtractiveSummary, AbstractiveSummary
from SummarizerToolWeb.db import db
from models.SummaryModel import Summary


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    user_id = session.get('user_id')
    input_text = session.get('input_text', '')
    summary_type = session.get('summary_type', 'Abstractive')
    summary_length = session.get('summary_length', '10')
    summary_text = session.get('summary_text', '')
    slider_index = session.get('slider_index','0')
    return render_template('index.html',
                           input_text=input_text,
                           summary_type=summary_type,
                           slider_value=summary_length,
                           slider_index=slider_index,
                           result_text=summary_text)


@bp.route('/submit', methods=['POST'])
def request_summary():
    input_text = request.form.get('hiddenTextValue')
    summary_type = request.form.get('hiddenSummaryType')
    summary_length_str = request.form.get('hiddenSliderValue')
    session['input_text'] = input_text
    session['summary_type'] = summary_type
    session['summary_length'] = summary_length_str

    summary_text = summarize(input_text, summary_type, summary_length_str)
    session['summary_text'] = summary_text

    history = session.get('history', [])
    history.append(summary_text)
    session['history'] = history

    mapping = {'10': '0', '25': '1', '35': '2', '50': '3'}
    slider_index = mapping.get(summary_length_str, '0')
    session['slider_index'] = slider_index

    new_summaryModel = Summary(
        session_id=session.get('user_id', None),  # or store cookie value if you wish
        input_text=input_text, 
        summary_type= "Abstraktyvus" if summary_type == "Abstractive" else "Ekstraktyvus",
        summary_text=summary_text
        # summary_length=summary_length_str
    )
    db.session.add(new_summaryModel)
    db.session.commit()

    return render_template('index.html',
                           input_text=input_text,
                           summary_type=summary_type,
                           slider_value=summary_length_str,
                           slider_index=slider_index,
                           result_text=summary_text)



@bp.route('/download', methods=['POST'])
def download_summary():
    summary_text = session.get('summary_text', '')
    summary_type = session.get('summary_type', '')
    input_text = session.get('input_text', '')

    csv_data = DownloadFormat.format_csv(input_text, summary_text, summary_type)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=summary_data.csv"}
    )

def summarize(input_text, summary_type, summary_length_str):
    if summary_type.lower() == 'abstractive':
        try:
            summary_text = AbstractiveSummary.summarize(input_text, summary_length_str)
        except Exception as e:
            summary_text = "Abstractive Summary generation was unsuccessful! :("
            print(f"GGGG: {str(e)}")

    elif summary_type.lower() == 'extractive':
        print('== main_controller.ExtractiveSummary.summarize() ==')
        summary_text = ExtractiveSummary.summarize(input_text, summary_length_str)
    else:
        raise TypeError

    return summary_text


@bp.route('/debug/summaries')
def debug_summaries():
    all_summaries = Summary.query.all()
    data = [{
        'id':      s.id,
        'user_id': s.session_id,
        'input':   s.input_text,
        'type':    s.summary_type,
        'summary': s.summary_text
    } for s in all_summaries]
    return jsonify(data)

