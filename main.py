import getPDF
import sendMail



def main():
    pdf = getPDF.getPdf()
    mail = sendMail.SendMail()
    pdf.get_apphealth()
    mail.run()



if __name__ == '__main__':
    main()

