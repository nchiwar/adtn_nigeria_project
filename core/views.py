from django.shortcuts import render
from news.models import NewsItem
from .models import CpdArticle, About
import logging

def home(request):
    news_items = NewsItem.objects.all()[:3]
    cpd_articles = CpdArticle.objects.all()[:3]
    context = {
        'news_items': news_items,
        'news_loading': False,
        'cpd_articles': cpd_articles,
        'cpd_loading': False,
    }
    return render(request, 'core/home.html', context)

def news_list(request):
    return render(request, 'news/news_list.html')

def placeholder(request):
    return render(request, 'core/placeholder.html', {'message': 'This page is under construction.'})

# Set up logging
logger = logging.getLogger(__name__)

def about(request):
    about_data = About.objects.first()  # Assuming About model stores this data
    context = {
        'about_description': about_data.about_description if about_data else "Loading...",
        'mission': about_data.mission if about_data else "Loading...",
        'vision': about_data.vision if about_data else "Loading...",
        'core_values': about_data.core_values if about_data else "Loading...",
        'goals': about_data.goals if about_data else "Loading...",
        'history_summary': about_data.history_summary if about_data else "Loading...",
        'formation_summary': about_data.formation_summary if about_data else "Loading...",
    }
    if about_data and about_data.goals:
        context['goals_list'] = [goal.strip() for goal in about_data.goals.replace('\\n', '\n').split('\n') if goal.strip()]
        logger.debug(f"goals_list: {context['goals_list']}")
    else:
        context['goals_list'] = ["Loading..."]
    return render(request, 'core/about.html', context)

def history(request):
    # Detailed history content from Flutter code
    history_content = """
    Nigeria does not really have recorded events on orthodox dental practice as in Europe, Asia and America. However oral history had it that the Agatu tribe in Benue State of the middle belt in Nigeria used bones and wires to replace teeth. As it were, the recorded event about Dental Technology in Nigeria followed the end of 2nd World War in 1946 when one Mr. S.E. Baker was deployed to the Royal Army Dental Corps Unit in Lagos.

    In 1953, the Western Regional Production Development Board in Ibadan advertised to send people on course which attracted many applicants. When the selection and interview was completed in March 1954, five candidates emerged successfully to study Dental technology. These candidates were Mr. Akadri (who retired as a Lt Col in the Nigerian Army), Mr. Adetunji, Mr. Akila, Mr. Anokwu and Mrs Ashogbon.

    Unfortunately their deployment for study in suitable institution was futile in 1954. However the dental mechanic instructor at Broad Street Lagos Mr. S.E Baker was contacted privately to assist in coaching these students. This was almost towards the end of 1955.

    Through his advice and assistance instead of training privately in Lagos, arrangement was made on how these five students will travel to United Kingdom to study Dental Mechanics. This arrangement was concluded by October 1955 and by November 1955 they finally departed to Britain for the programme.

    It was at Rutherford College of Technology in Britain that they were admitted for their course of study and involved in practical work, under Mr. H Feartherstone’s Dental laboratory in Newcastle Upon-Tyne.

    At Newcastle it was discovered that two year earlier some students from other parts of Nigeria have written their City and Guild intermediate. These students and one Mr. G. Otigba were very instrumental to those boys admission. Pa Eldred Efiok Eyo a Federal Government candidate was also very helpful to them and other student from Ghana and Liberia.

    Pa Efiok Eyo is an indelible name in the history of Dental Technology to the extent that he became the first Nigerian Dental Technologist and later the first indigenous chief instructor at the Federal School of Dental Technology at No 1 Broad Street Lagos.
    """
    change_designation = """
    At Rutherford College, efforts were made to change the designation through Mr. H. Feartherstone from Dental mechanics to Dental Technology. Although this was approved then but not effected at the dismay of the students when they came back to Nigeria in 1960.
    """
    salary_scale = """
    The salary grade known as CT 2, 3, 4 for Technologist graduates was a struggle by those students while in United Kingdom. The Regional government in Nigeria granted this. Along the line the cancellation of 50% commission to surgeons and dash given by surgery to technologist was also fought for and later this was cancelled. As at now the grade level of fresh graduate of Dental Technology in the civil service scale is level 08.
    """
    training_institutions = """
    In 1955 the first training institute for Dental Technology was established at No. 1 Broad street Lagos.

    This school was moved to Enugu in 1982 and is now designated Federal school of Dental Technology and Therapy Trans Ekulu, Enugu State. About 400 Nigerians, 2 Senegalese, 5 Gambians and 15 Ghanaians have graduated as Dental Technologist from the school as of 1993.

    It was also recorded that in 1970 the Armed forces established an institution at Military Hospital Yaba Lagos. The Army institution was later moved to their permanent site in 1977 at Nigerian Army cantonment Ojo Lagos.

    The school was accredited for city and Guild Examinations Centre in 1984 and award for HND in 2003 by the National Board for Technical Education (NBTE).

    It is equally important to note that by 1961 and 1964 the expatriates heading the institution at Broad Street were replaced by the Nigerian who had trained in the United Kingdom.

    Furthermore, the profession of Dental Technology witnessed a new dawn of advancement with the Federal University of Technology Owerri, Imo State establishing the department of dental technology in 2003 for the award of Bachelor of Technology (B.Tech) degree in dental technology.

    Information also has it that some states of the federation have started establishing department of dental technology in their various schools/colleges of health technologies.

    Presently, the institutions offering Dental Technology in Nigeria are as follows:
    1. Federal School of Dental Technology and Therapy, Tran-Ekulu, Enugu State established in 1955 as the first training institution in No. 1 Broad Street Lagos but later moved to present location in Enugu (HND awarding).
    2. Nigerian Army School of Medical Sciences, Military Cantonment Ojo, Lagos State established in 1970 (HND awarding).
    3. Federal University of Technology, Owerri established in 2002 following approval granted by the National Universities Commission (NUC). (Degree awarding).
    4. Ogun State College of Health Technology Ilesse Ijebu-ode, Ogun State established in 2007 (HND awarding).
    5. Shehu Idris College of Health Technology, Markarfi, Kaduna State established in 2009 (HND awarding).
    6. Kwara State College of Health Technology, Offa, Kwara State established in 2013 (HND awarding).
    """

    context = {
        'history_content': history_content,
        'change_designation': change_designation,
        'salary_scale': salary_scale,
        'training_institutions': training_institutions,
    }
    return render(request, 'core/history.html', context)

def formation_adtn(request):
    # Placeholder content for Formation of ADTN (to be expanded with actual data)
    formation_content = """
    The increase in awareness of the services of the dental technologists after the return of the first Nigerian Dental technologist who trained abroad and the necessity for a common fight for the right and benefits of the professionals in the health sector both at federal and state levels prompted the formation of the Association of Dental Technologists of Nigeria (ADTN).
The Association was as a result of like minds in the profession having the need for pursuit of the goals and objectives of the profession as a common body and also protection of the interest of the profession.
Though in existence, the Association did not have any secretariat until 1976 when for logistic reasons a mini secretariat was carved out at the School of Dental Science, College of Medicine, and Lagos University Teaching Hospital (CMUL/LUTH) Idi-araba, Lagos.
As it were these gentle men and ladies started making more positive impacts in the health sector and even to the government bodies as the need and importance of Dental Technology arose in the society. With their individual and collective efforts with meager resources available they pressurized to various tribunals and commissions for signing the profession into law for full government recognition.
This effort was a great success as it gave birth to the Dental Technologists Registration Board of Nigeria (DTRBN) with its motto called “For Beauty and Function”.
The objectives of the Association include:

To promote the art, science and practice of the profession of Dental Technology and Allied Subjects.
To facilitate and or ensure the exchange of information, experience and ideas on matters affecting the practice, science and art of Dental Technology.
To promote and maintain the general welfare and conditions of practice of the profession of Dental Technology.
To create and hold funds, which shall be available for furthering the objectives of the Association.
To promote national and international co-operation in all fields of science, art and practice of Dental Technology and its allied subjects.
To promote research and development that will enhance the practice of dental technology.
To establish a structure that encourages effective coordination of members of the Association throughout Nigeria.
To liaise with other international Association on best practices for the profession worldwide.
To sensitize members on current innovations in dental technology through regular publications.
To liaise with the Board regularly on issues bordering improvement of the profession.
    """
    context = {
        'formation_content': formation_content,
    }
    return render(request, 'core/formation_adtn.html', context)