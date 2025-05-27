from flask import Blueprint, render_template, session, Response
from models.SummaryModel import Summary
from services import DownloadFormat
from SummarizerToolWeb.db import db

bp = Blueprint('history', __name__)

@bp.route('/history')
def history():
    summaries = get_all_summaries()

    return render_template('history.html', Summary_History=summaries)


@bp.route('/history', methods=['POST'])
def delete_history_item(item_id):
    item = Summary.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    history()


@bp.route('/history/download_item/<int:item_id>', methods=['POST'])
def download_item(item_id):
    summary = Summary.query.get_or_404(item_id)

    csv_data = DownloadFormat.format_csv(
        summary.input_text, summary.summary_text, summary.summary_type
    )

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=summary_data.csv"}
    )


@bp.route('/history/download_all', methods=['POST'])
def download_all():
    summaries = get_all_summaries()

    csv_data = DownloadFormat.format_list_csv(summaries)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=summary_history.csv"}
    )



def get_all_summaries():
    uid = session['user_id']
    summaries = (
        Summary.query
                .filter_by(session_id=uid)
                .order_by(Summary.id.desc())
                .all()
    )
    return summaries
