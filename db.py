from app import db, Doc

fl_desc = " Flask is a micro webdevelopment framework for Python. You are currently looking at the documentation of the development version. "
fl_sect = [
  {
    "title": "Introduction",
    "content": [
      {
        "title": "What does 'micro' mean?",
        "text": '''
                'Micro' does not mean that your whole web application has to fit into a
                single Python file, although it certainly can. Nor does it mean that Flask
                is lacking in functionality. The 'micro' in microframework means Flask aims 
                to keep the core simple but extensible. Flask won't make many decisions for you,
                such as what database to use. Those decisions that it does make, such as what 
                templating engine to use, are easy to change. Everything else is up to you, so 
                that Flask can be everything you need and nothing you don't.
                '''
      },
      {
        "title": "Configuration and Conventions",
        "text": "Flask has many configuration values, with sensible defaults, and a few conventions when getting started. By convention templates and static files are stored in subdirectories within the application's Python source tree, with the names templates and static respectively. While this can be changed you usually don't have to, especially when getting started."
      },
      {
        "title": "Growing with Flask",
        "text": "Once you have Flask up and running, you'll find a variety of extensions available in the community to integrate your project for production. The Flask core team reviews extensions and ensures approved extensions do not break with future releases. As your codebase grows, you are free to make the design decisions appropriate for your project. Flask will continue to provide a very simple glue layer to the best that Python has to offer. You can implement advanced patterns in SQLAlchemy or another database tool, introduce non-relational data persistence as appropriate, and take advantage of framework-agnostic tools built for WSGI, the Python web interface."
      }
    ]
  }
]

rails_description = ''' Rails is a web application development framework written in the Ruby language. It is designed to make programming web applications easier by making assumptions about what every developer needs to get started. It allows you to write less code while accomplishing more than many other languages and frameworks. Experienced Rails developers also report that it makes web application development more fun. '''
rails_sections = [
  {
    "title": "Getting Started with Rails",
    "content": [
      {
        "title": "1 Guide Assumptions",
        "text": 
          '''This guide is designed for beginners who want to get started with a Rails application from scratch. It does not assume that you have any prior experience with Rails. However, to get the most out of it, you need to have some prerequisites installed:

          The Ruby language version 1.9.3 or newer.
          The RubyGems packaging system, which is installed with Ruby versions 1.9 and later. To learn more about RubyGems, please read the RubyGems Guides.
          A working installation of the SQLite3 Database.
          Rails is a web application framework running on the Ruby programming language. If you have no prior experience with Ruby, you will find a very steep learning curve diving straight into Rails. There are several curated lists of online resources for learning Ruby:

          Official Ruby Programming Language website
          reSRC's List of Free Programming Books
          Be aware that some resources, while still excellent, cover versions of Ruby as old as 1.6, and commonly 1.8, and will not include some syntax that you will see in day-to-day development with Rails.
          '''
      },
      {
        "title": "2 What is Rails?",
        "text": '''
          Rails is a web application development framework written in the Ruby language. It is designed to make programming web applications easier by making assumptions about what every developer needs to get started. It allows you to write less code while accomplishing more than many other languages and frameworks. Experienced Rails developers also report that it makes web application development more fun.

          Rails is opinionated software. It makes the assumption that there is the "best" way to do things, and it's designed to encourage that way - and in some cases to discourage alternatives. If you learn "The Rails Way" you'll probably discover a tremendous increase in productivity. If you persist in bringing old habits from other languages to your Rails development, and trying to use patterns you learned elsewhere, you may have a less happy experience.

          The Rails philosophy includes two major guiding principles:

          Don't Repeat Yourself: DRY is a principle of software development which states that "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." By not writing the same information over and over again, our code is more maintainable, more extensible, and less buggy.
          Convention Over Configuration: Rails has opinions about the best way to do many things in a web application, and defaults to this set of conventions, rather than require that you specify every minutiae through endless configuration files.
        '''
      },
      {
        "title": "3 Creating a New Rails Project",
        "text": '''
          The best way to use this guide is to follow each step as it happens, no code or step needed to make this example application has been left out, so you can literally follow along step by step. You can get the complete code here.

          By following along with this guide, you'll create a Rails project called blog, a (very) simple weblog. Before you can start building the application, you need to make sure that you have Rails itself installed.

          The examples below use $ to represent your terminal prompt in a UNIX-like OS, though it may have been customized to appear differently. If you are using Windows, your prompt will look something like c:\source_code>
        '''
      }
    ]
  }
]

flask = Doc(title='Flask', language='en', version='0.10.1', description=fl_desc, sections=fl_sect)
db.session.add(flask)

rails = Doc(title='Ruby on Rails', language='en', version='4.1.1', description=rails_description, sections=rails_sections)
db.session.add(rails)

db.session.commit()




