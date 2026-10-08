from flask import Flask, render_template, send_file, redirect, url_for, request
from analyser import Analyser
from services.date_service import get_previous_month, get_year_of_previous_month
from services.version_service import get_application_version, get_author
from exceptions.analyser_exception import AnalyserException
from exceptions.collector_exception import CollectorException
from services.configuration_provider import get_project_configuration
from services.counter import get_generated_analysis_counter_value, increment_counters, get_time_saved, get_total_time_saved
from services.stopper import  start_stopper, end_stopper

app = Flask(__name__)

configuration = get_project_configuration('MAIN')
analyser = None

def export_analysis(format):
   output_file_pathname = analyser.export_analysis(format)
   number_of_matching_tickets = analyser.get_number_of_matching_tickets()
   increment_counters(analyser.year, analyser.month, analyser.project_identifier, number_of_matching_tickets)
   return output_file_pathname

def export_protocol():
   output_file_pathname = analyser.export_protocol()
   return output_file_pathname

def analyze(request, project):
   project_identifier = str(project)
   api_key = str(request.form['api_key'])
   year = int(request.form['year'])
   month = int(request.form['month'])
   raport_file_pathname = save_raport_and_return_file_pathname(request)
   
   global analyser
   analyser = Analyser(api_key=api_key, year=year, month=month, project_identifier=project_identifier,
                       raport_file_pathname=raport_file_pathname)
   analyser.analyze()
   
def save_raport_and_return_file_pathname(request):
   try:
      directory_for_raport_files = configuration['path']['raport']['input']
      raport_file = request.files['raport']
      raport_file_name = raport_file.filename
      raport_file_full_pathname = directory_for_raport_files + raport_file_name
      raport_file.save(raport_file_full_pathname)
      return raport_file_full_pathname
   except Exception:
      cause="Brak raportu od wykonawcy."
      advice="Aby dokonać analizy, załącz raport od wykonawcy."
      raise CollectorException(cause=cause, advice=advice)
   
def is_project_supporting_protocol_generation(project_code):
   list_of_projects_supporting_protocol_generation = configuration['projects_supporting_protocol_generation']
   if project_code in list_of_projects_supporting_protocol_generation:
      return True
   else:
      return False
   
@app.context_processor
def inject_application_version():
   return dict(application_version=get_application_version(), application_author=get_author())
   
@app.route('/')
def home():
   count_of_generated_analysis= get_generated_analysis_counter_value()
   time_saved = get_total_time_saved()
   return render_template('home.html',count_of_analysis=count_of_generated_analysis, time_saved=time_saved)

@app.route('/project_list')
def select_project():
   start_stopper()
   return render_template('project_list.html')

@app.route('/<project>/specifications',  methods = ['POST', 'GET'])
def select_date_and_raport_and_api_key(project):
   if request.method == 'GET':
      previous_month = get_previous_month()
      year_of_previous_month = get_year_of_previous_month()
      return render_template('specifications.html',selected_project=project, suggested_month=previous_month, suggested_year=year_of_previous_month)
   else:
      try:
         analyze(request=request,project=project)
         return redirect(url_for('select_export_raport_format_or_protocol', project=project))
      except AnalyserException as exception:
         return render_template('error.html', exception=exception)
         
@app.route('/<project>/export_format')
def select_export_raport_format_or_protocol(project):
   support_protcol_generation = is_project_supporting_protocol_generation(project)
   time_taken = end_stopper()
   time_saved = get_time_saved(analyser.get_number_of_matching_tickets())
   return render_template('export_raport_or_protocol.html', total_time_taken=time_taken, time_saved=time_saved, protocol_support=support_protcol_generation)

@app.route('/raport/<format>')
def download_raport(format):
   try:
      output_file_pathname = export_analysis(format)
      return send_file(path_or_file=output_file_pathname)
   except AnalyserException as exception:
      return render_template('error.html', exception=exception)
   
@app.route('/protocol')
def download_protocol():
   try:
      output_file_pathname = export_protocol()
      return send_file(path_or_file=output_file_pathname)
   except AnalyserException as exception:
      return render_template('error.html', exception=exception)
   
@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/user_documentation')
def user_documentation():
   return render_template('user_documentation.html',user_page_active="active")

@app.route('/developer_documentation')
def developer_documentation():
   return render_template('developer_documentation.html',dev_page_active="active")

@app.route('/configuration_documentation')
def configuration_documentation():
   return render_template('configuration_documentation.html',config_page_active="active")

app.run()