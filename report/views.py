import datetime
import pandas as pd
import zipfile
from io import BytesIO

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.db.models import Q


from metrics.models import Metric, Project
from report.models import LearningArea, EvaluationObjective, Editor, Organizer, Partner, \
    Funding, Technology, Report, AreaActivated, Activity
from users.models import TeamArea, UserProfile
from report.forms import NewReportForm, activities_associated_as_choices,\
    AreaActivatedForm, FundingForm, PartnerForm, TechnologyForm


# CREATE
@login_required
@permission_required("report.add_report")
def add_report(request):
    report_form = NewReportForm(request.POST or None, user=request.user)
    directions_related_set = list(map(int, report_form.data.getlist('directions_related', [])))
    learning_questions_related_set = list(map(int, report_form.data.getlist('learning_questions_related', [])))
    metrics_set = list(map(int, report_form.data.getlist('metrics_related', [])))
    if request.method == "POST":
        if report_form.is_valid():
            report = report_form.save(user=request.user)

            messages.success(request, _("Report registered successfully!"))
            return redirect(reverse("report:detail_report", kwargs={"report_id": report.id}))

        else:
            messages.error(request, _("Something went wrong!"))
            for field, error in report_form.errors.items():
                messages.error(request, field + ": " + error[0])
            context = {
                "directions_related_set": directions_related_set,
                "learning_questions_related_set": learning_questions_related_set,
                "metrics_set": metrics_set,
                "report_form": report_form
            }
            return render(request, "report/add_report.html", context)
    else:
        context = {"directions_related_set": directions_related_set,
                   "learning_questions_related_set": learning_questions_related_set,
                   "metrics_set": metrics_set,
                   "report_form": report_form}

        return render(request, "report/add_report.html", context)


@login_required
@permission_required("report.add_areaactivated")
def add_area_activated(request):
    area_form = AreaActivatedForm(request.POST or None)
    if request.method == "POST":
        if area_form.is_valid():
            area, created = AreaActivated.objects.get_or_create(text=area_form.cleaned_data['text'])
            return JsonResponse({"id": area.id, "text": area.text})
        else:
            return JsonResponse({"id": None})
    else:
        context = {"area_form": area_form}
        return render(request, "area_activated/add_area.html", context)


@login_required
@permission_required("report.add_funding")
def add_funding(request):
    funding_associated_form = FundingForm(request.POST or None)
    if request.method == "POST":
        if funding_associated_form.is_valid():
            funding, created = Funding.objects.get_or_create(name=funding_associated_form.cleaned_data["name"], value=funding_associated_form.cleaned_data["value"], project=funding_associated_form.cleaned_data["project"])
            return JsonResponse({"id": funding.id, "text": funding.name})
        else:
            return JsonResponse({"id": None, "text": None})
    else:
        context = {"funding_form": funding_associated_form}
        return render(request, "funding/add_funding.html", context)


@login_required
@permission_required("report.add_partner")
def add_partner(request):
    partner_form = PartnerForm(request.POST or None)
    if request.method == "POST":
        if partner_form.is_valid():
            partner, created = Partner.objects.get_or_create(name=partner_form.cleaned_data["name"])
            return JsonResponse({"id": partner.id, "text": partner.name})
        else:
            return JsonResponse({"id": None, "text": None})
    else:
        context = {"partner_form": partner_form}
        return render(request, "partners/add_partner.html", context)


@login_required
@permission_required("report.add_technology")
def add_technology(request):
    technology_form = TechnologyForm(request.POST or None)
    if request.method == "POST":
        if technology_form.is_valid():
            technology, created = Technology.objects.get_or_create(name=technology_form.cleaned_data["name"])
            return JsonResponse({"id": technology.id, "text": technology.name})
        else:
            return JsonResponse({"id": None, "text": None})
    else:
        context = {"technology_form": technology_form}
        return render(request, "technologies/add_technology.html", context)


# REVIEW
@login_required
@permission_required("report.view_report")
def list_reports(request):
    context = {"dataset": Report.objects.order_by('-created_at'), "mine": False}

    return render(request, "report/list_reports.html", context)


@login_required
@permission_required("report.view_report")
def detail_report(request, report_id):
    context = {"data": Report.objects.get(id=report_id)}

    return render(request, "report/detail_report.html", context)


def add_csv_file(function_name, report_id=None):
    csv_file = BytesIO()
    function_name(report_id).to_csv(path_or_buf=csv_file, index=False)

    return csv_file


def add_excel_file(report_id=None):
    excel_file = BytesIO()
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    export_report_instance(report_id).to_excel(writer, sheet_name='Report', index=False)
    export_metrics(report_id).to_excel(writer, sheet_name='Metrics', index=False)
    export_user_profile(report_id).to_excel(writer, sheet_name='Users', index=False)
    export_area_activated(report_id).to_excel(writer, sheet_name='Areas', index=False)
    export_directions_related(report_id).to_excel(writer, sheet_name='Directions', index=False)
    export_editors(report_id).to_excel(writer, sheet_name='Editors', index=False)
    export_learning_questions_related(report_id).to_excel(writer, sheet_name='Learning questions', index=False)
    export_organizers(report_id).to_excel(writer, sheet_name='Organizers', index=False)
    export_partners_activated(report_id).to_excel(writer, sheet_name='Partners', index=False)
    export_technologies_used(report_id).to_excel(writer, sheet_name='Technologies', index=False)

    writer.close()
    return excel_file


@login_required
@permission_required("report.view_report")
def export_report(request, report_id=None):
    buffer = BytesIO()
    zip_file = zipfile.ZipFile(buffer, mode="w")
    sub_directory = "csv/"

    if report_id:
        zip_name = _("Report")
        identifier = " {}".format(report_id)
    else:
        zip_name = _("SARA - Reports")
        identifier = ""

    posfix = identifier + " - {}".format(datetime.datetime.today().strftime('%Y-%m-%d'))
    files = [[export_report_instance, sub_directory + 'Report' + posfix],
             [export_metrics, sub_directory + 'Metrics' + posfix],
             [export_user_profile, sub_directory + 'Users' + posfix],
             [export_area_activated, sub_directory + 'Areas' + posfix],
             [export_directions_related, sub_directory + 'Directions' + posfix],
             [export_editors, sub_directory + 'Editors' + posfix],
             [export_learning_questions_related, sub_directory + 'Learning questions' + posfix],
             [export_organizers, sub_directory + 'Organizers' + posfix],
             [export_partners_activated, sub_directory + 'Partners' + posfix],
             [export_technologies_used, sub_directory + 'Technologies' + posfix]]

    for file in files:
        zip_file.writestr('{}.csv'.format(file[1]), add_csv_file(file[0], report_id).getvalue())
    zip_file.writestr('Export' + posfix + '.xlsx', add_excel_file(report_id).getvalue())

    zip_file.close()

    response = HttpResponse(buffer.getvalue())
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment; filename=' + zip_name + posfix + '.zip'

    return response


def export_report_instance(report_id=None):
    header = [_('ID'), _('Created by'), _('Created at'), _('Modified by'), _('Modified at'), _('Activity associated'),
              _('Name of the activity'), _('Area responsible'), _('Area activated'), _('Initial date'), _('End date'),
              _('Description'), _('Funding associated'), _('Links'), _('Public communication'),
              _('Number of participants'), _('Number of resources'), _('Number of feedbacks'), _('Editors'),
              _('Organizers'), _('Partnerships activated'), _('Technologies used'), _('# Wikipedia created'),
              _('# Wikipedia edited'), _('# Commons created'), _('# Commons edited'), _('# Wikidata created'),
              _('# Wikidata edited'), _('# Wikiversity created'), _('# Wikiversity edited'), _('# Wikibooks created'),
              _('# Wikibooks edited'), _('# Wikisource created'), _('# Wikisource edited'), _('# Wikinews created'),
              _('# Wikinews edited'), _('# Wikiquote created'), _('# Wikiquote edited'), _('# Wiktionary created'),
              _('# Wiktionary edited'), _('# Wikivoyage created'), _('# Wikivoyage edited'), _('# Wikispecies created'),
              _('# Wikispecies edited'), _('# Metawiki created'), _('# Metawiki edited'), _('# MediaWiki created'),
              _('# MediaWiki edited'), _('Directions related'), _('Learning'), _('Learning questions related')]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        # Database
        id_ = report.id
        created_by = report.created_by.id
        created_at = report.created_at
        modified_by = report.modified_by.id
        modified_at = report.modified_at

        # Administrative
        activity_associated = report.activity_associated.id
        activity_other = report.activity_other or ""
        area_responsible = report.area_responsible.id
        if report.area_activated.exists():
            area_activated = "; ".join(map(str, report.area_activated.values_list("id", flat=True)))
        else:
            area_activated = ""
        initial_date = report.initial_date
        end_date = report.end_date
        description = report.description
        if report.funding_associated.exists():
            funding_associated = "; ".join(map(str, report.funding_associated.values_list("id", flat=True)))
        else:
            funding_associated = ""
        links = report.links.replace("\r\n", "; ")
        public_communication = report.public_communication

        # Quantitative
        participants = report.participants
        resources = report.resources
        feedbacks = report.feedbacks
        if report.editors.exists():
            editors = "; ".join(map(str, report.editors.values_list("id", flat=True)))
        else:
            editors = ""
        if report.organizers.exists():
            organizers = "; ".join(map(str, report.organizers.values_list("id", flat=True)))
        else:
            organizers = ""
        if report.partners_activated.exists():
            partners_activated = "; ".join(map(str, report.partners_activated.values_list("id", flat=True)))
        else:
            partners_activated = ""
        if report.technologies_used.exists():
            technologies_used = "; ".join(map(str, report.technologies_used.values_list("id", flat=True)))
        else:
            technologies_used = ""

        # Wikimedia
        wikipedia_created = report.wikipedia_created
        wikipedia_edited = report.wikipedia_edited
        commons_created = report.commons_created
        commons_edited = report.commons_edited
        wikidata_created = report.wikidata_created
        wikidata_edited = report.wikidata_edited
        wikiversity_created = report.wikiversity_created
        wikiversity_edited = report.wikiversity_edited
        wikibooks_created = report.wikibooks_created
        wikibooks_edited = report.wikibooks_edited
        wikisource_created = report.wikisource_created
        wikisource_edited = report.wikisource_edited
        wikinews_created = report.wikinews_created
        wikinews_edited = report.wikinews_edited
        wikiquote_created = report.wikiquote_created
        wikiquote_edited = report.wikiquote_edited
        wiktionary_created = report.wiktionary_created
        wiktionary_edited = report.wiktionary_edited
        wikivoyage_created = report.wikivoyage_created
        wikivoyage_edited = report.wikivoyage_edited
        wikispecies_created = report.wikispecies_created
        wikispecies_edited = report.wikispecies_edited
        metawiki_created = report.metawiki_created
        metawiki_edited = report.metawiki_edited
        mediawiki_created = report.mediawiki_created
        mediawiki_edited = report.mediawiki_edited

        # Strategy
        if report.directions_related.exists():
            directions_related = "; ".join(map(str, report.directions_related.values_list("id", flat=True)))
        else:
            directions_related = ""
        learning = report.learning.replace("\r\n", "\n")

        # Theory
        if report.learning_questions_related.exists():
            learning_questions_related = "; ".join(map(str, report.learning_questions_related.values_list("id", flat=True)))
        else:
            learning_questions_related = ""

        rows.append([id_, created_by, created_at, modified_by, modified_at, activity_associated, activity_other,
                     area_responsible, area_activated, initial_date, end_date, description, funding_associated, links,
                     public_communication, participants, resources, feedbacks, editors,
                     organizers, partners_activated, technologies_used, wikipedia_created, wikipedia_edited,
                     commons_created, commons_edited, wikidata_created, wikidata_edited, wikiversity_created,
                     wikiversity_edited, wikibooks_created, wikibooks_edited, wikisource_created, wikisource_edited,
                     wikinews_created, wikinews_edited, wikiquote_created, wikiquote_edited, wiktionary_created,
                     wiktionary_edited, wikivoyage_created, wikivoyage_edited, wikispecies_created, wikispecies_edited,
                     metawiki_created, metawiki_edited, mediawiki_created, mediawiki_edited, directions_related,
                     learning, learning_questions_related])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()

    df[_('Created at')] = df[_('Created at')].dt.tz_localize(None)
    df[_('Modified at')] = df[_('Modified at')].dt.tz_localize(None)
    return df


def export_metrics(report_id=None):
    header = [_('ID'), _('Metric'), _('Activity ID'), _('Activity'), _('Activity code'), _('Number of editors'),
              _('Number of participants'), _('Number of partnerships'), _('Number of resources'),
              _('Number of feedbacks'), _('Number of events'), _('Other type? Which?'), _('Observation'),
              _('# Wikipedia created'), _('# Wikipedia edited'), _('# Commons created'), _('# Commons edited'),
              _('# Wikidata created'), _('# Wikidata edited'), _('# Wikiversity created'), _('# Wikiversity edited'),
              _('# Wikibooks created'), _('# Wikibooks edited'), _('# Wikisource created'), _('# Wikisource edited'),
              _('# Wikinews created'), _('# Wikinews edited'), _('# Wikiquote created'), _('# Wikiquote edited'),
              _('# Wiktionary created'), _('# Wiktionary edited'), _('# Wikivoyage created'), _('# Wikivoyage edited'),
              _('# Wikispecies created'), _('# Wikispecies edited'), _('# Metawiki created'), _('# Metawiki edited'),
              _('# MediaWiki created'), _('# MediaWiki edited')]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        if report.activity_associated:
            for instance in report.activity_associated.metrics.all():
                rows.append([instance.id, instance.text, instance.activity_id, instance.activity.text,
                             instance.activity.code, instance.number_of_editors, instance.number_of_participants,
                             instance.number_of_partnerships, instance.number_of_resources, instance.number_of_feedbacks,
                             instance.number_of_events, instance.other_type, instance.observation,
                             instance.wikipedia_created, instance.wikipedia_edited, instance.commons_created,
                             instance.commons_edited, instance.wikidata_created, instance.wikidata_edited,
                             instance.wikiversity_created, instance.wikiversity_edited, instance.wikibooks_created,
                             instance.wikibooks_edited, instance.wikisource_created, instance.wikisource_edited,
                             instance.wikinews_created, instance.wikinews_edited, instance.wikiquote_created,
                             instance.wikiquote_edited, instance.wiktionary_created, instance.wiktionary_edited,
                             instance.wikivoyage_created, instance.wikivoyage_edited, instance.wikispecies_created,
                             instance.wikispecies_edited, instance.metawiki_created, instance.metawiki_edited,
                             instance.mediawiki_created, instance.mediawiki_edited])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()
    return df


def export_user_profile(report_id=None):
    header = [_('ID'), _('First name'), _('Last Name'), _('Username on Wiki (WMB)'), _('Username on Wiki'),
              _('Photograph'), _('Position'), _('Twitter'), _('Facebook'), _('Instagram'), _('Email'),
              _('Wikidata item'), _('LinkedIn'), _('Lattes'), _('Orcid'), _('Google_scholar')]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        for instance in [report.created_by, report.modified_by]:
            rows.append([instance.id,
                         instance.user.first_name or "",
                         instance.user.last_name or "",
                         instance.professional_wiki_handle or "",
                         instance.personal_wiki_handle or "",
                         instance.photograph or "",
                         instance.position or "",
                         instance.twitter or "",
                         instance.facebook or "",
                         instance.instagram or "",
                         instance.user.email or "",
                         instance.wikidata_item or "",
                         instance.linkedin or "",
                         instance.lattes or "",
                         instance.orcid or "",
                         instance.google_scholar or ""])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()
    return df


def export_area_activated(report_id=None):
    header = [_('ID'), _('Area activated'), _('Contact')]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        for instance in report.area_activated.all():
            rows.append([instance.id, instance.text, instance.contact])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()
    return df


def export_directions_related(report_id=None):
    header = [_('ID'), _('Direction related'), _('Strategic axis ID'), _('Strategic axis text')]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        for instance in report.directions_related.all():
            rows.append([instance.id, instance.text, instance.strategic_axis_id, instance.strategic_axis.text])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()
    return df


def export_editors(report_id=None):
    header = [_('ID'), _('Username')]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        for instance in report.editors.all():
            rows.append([instance.id, instance.username])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()
    return df


def export_learning_questions_related(report_id=None):
    header = [_('ID'), _('Learning question'), _('Learning area ID'), _('Learning area')]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        for instance in report.learning_questions_related.all():
            rows.append([instance.id, instance.text, instance.learning_area_id, instance.learning_area.text])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()
    return df


def export_organizers(report_id=None):
    header = [_('ID'), _("Organizer's name"), _("Organizer's institution ID"), _("Organizer institution's name")]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        for instance in report.organizers.all():
            rows.append([instance.id, instance.name, ";".join(map(str, instance.institution.values_list("id", flat=True))), ";".join(map(str, instance.institution.values_list("name", flat=True)))])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()
    return df


def export_partners_activated(report_id=None):
    header = [_('ID'), _("Partners"), _("Partner's website")]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        for instance in report.partners_activated.all():
            rows.append([instance.id, instance.name, instance.website])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()
    return df


def export_technologies_used(report_id=None):
    header = [_('ID'), _("Technology")]

    if report_id:
        reports = Report.objects.filter(pk=report_id)
    else:
        reports = Report.objects.all()

    rows = []
    for report in reports:
        for instance in report.technologies_used.all():
            rows.append([instance.id, instance.name])

    df = pd.DataFrame(rows, columns=header).drop_duplicates()
    return df


# UPDATE
@login_required
@permission_required("report.change_report")
def update_report(request, report_id):
    obj = get_object_or_404(Report, id=report_id)
    if request.method == "POST":
        report_form = NewReportForm(request.POST or None, instance=obj, user=request.user)
        if report_form.is_valid():
            report_instance = report_form.save(commit=False)

            # Editors
            editors = get_or_create_editors(request.POST["editors_string"])
            report_instance.editors.set(editors)

            # Organizers
            organizers = get_or_create_organizers(request.POST["organizers_string"])
            report_instance.organizers.set(organizers)

            # Modified by and Modified at
            user_profile = UserProfile.objects.get(user=request.user)
            report_instance.modified_by = user_profile
            report_instance.modified_at = datetime.datetime.now()

            # Fundings
            fundings_associated = report_form.cleaned_data["funding_associated"]
            report_instance.funding_associated.set(fundings_associated)

            # Areas activated
            areas_activated = report_form.cleaned_data["area_activated"]
            report_instance.area_activated.set(areas_activated)

            # Partners
            partners_activated = report_form.cleaned_data["partners_activated"]
            report_instance.partners_activated.set(partners_activated)

            # Technologies
            technologies_used = report_form.cleaned_data["technologies_used"]
            report_instance.technologies_used.set(technologies_used)

            # Directions
            directions_related = report_form.cleaned_data["directions_related"]
            report_instance.directions_related.set(directions_related)

            # Learning Questions
            learning_questions_related = report_form.cleaned_data["learning_questions_related"]
            report_instance.learning_questions_related.set(learning_questions_related)

            # Metrics
            metrics_related = report_form.cleaned_data["metrics_related"]
            report_instance.metrics_related.set(metrics_related)

            report_instance.save()
            return redirect(reverse("report:detail_report", kwargs={"report_id": report_id}))
    else:
        report_form = NewReportForm(instance=obj, user=request.user)
        context = {"report_form": report_form,
                   "report_id": report_id,
                   "directions_related_set": list(obj.directions_related.values_list("id", flat=True)),
                   "learning_questions_related_set": list(obj.learning_questions_related.values_list("id", flat=True)),
                   "metrics_set": list(obj.metrics_related.values_list("id", flat=True))}
        return render(request, "report/update_report.html", context)


# DELETE
@login_required
@permission_required("report.delete_report")
def delete_report(request, report_id):
    report = Report.objects.get(id=report_id)
    context = {"report": report}

    if request.method == "POST":
        report.delete()
        return redirect(reverse('report:list_reports'))

    return render(request, 'report/delete_report.html', context)


# FUNCTIONS
def get_or_create_editors(editors_string):
    editors_list = editors_string.split("\r\n")
    editors = []
    if editors_string:
        for editor in editors_list:
            new_editor, created = Editor.objects.get_or_create(username=editor)
            if new_editor not in editors:
                editors.append(new_editor)

    return editors


def get_or_create_organizers(organizers_string):
    organizers_list = organizers_string.split("\r\n")
    organizers = []
    if organizers_string:
        for organizer in organizers_list:
            organizer_name, institution_name = (organizer + ";").split(";", maxsplit=1)
            new_organizer, new_organizer_created = Organizer.objects.get_or_create(name=organizer_name)
            if institution_name:
                for partner_name in institution_name.split(";"):
                    if partner_name:
                        partner, partner_created = Partner.objects.get_or_create(name=partner_name)
                        new_organizer.institution.add(partner)
                new_organizer.save()
            organizers.append(new_organizer)
    return organizers


def get_metrics(request):
    projects = []
    # ACTIVITY
    activity = request.GET.get("activity")
    if activity and activity != "1":
        activity_project = Project.objects.get(project_activity__activities=int(activity))
        metrics = Metric.objects.filter(activity_id=activity).values()
        projects.append({"project": activity_project.text, "metrics": list(metrics)})
    elif activity == "1":
        for project in Project.objects.all().exclude(pk=1):
            metrics = Metric.objects.filter(project=project).values()
            if metrics:
                projects.append({"project": project.text, "metrics": list(metrics)})
    # FUNDINGS
    fundings_ids = request.GET.getlist("fundings[]")
    projects_ids = Project.objects.filter(Q(project_related__in=fundings_ids))
    for project in projects_ids:
        metrics = Metric.objects.filter(project=project).values().order_by('text')
        projects.append({"project": project.text, "metrics": list(metrics)})
    # INSTANCE
    instance = request.GET.get("instance")
    if instance:
        metrics_ids = [metric["id"] for project in projects for metric in project["metrics"]]
        metrics_aux = Report.objects.get(pk=instance).metrics_related.all().values()
        metrics = [metric for metric in metrics_aux if metric["id"] not in metrics_ids]

        if metrics:
            projects.append({"project": _("Other metrics"), "metrics": list(metrics)})

    if projects:
        return JsonResponse({"objects": projects})
    else:
        return JsonResponse({"objects": None})
