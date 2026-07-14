import nodriver as uc
import time

async def main():
    driver = await uc.start()

    tab = await driver.get("https://ais.iitp.ac.in/moodle/")
    try:
        await driver.cookies.load()
        print("loaded cookies from .session.dat")
    except:
        print("failed to load cookies from .session.dat")

    print("waiting for the page to load")
    await tab.wait(5)

    try:
        print('finding the "Log in" button')
        Log_in = await tab.find("Log in", best_match=True)

        print('"Log in" => click')
        await Log_in.click()

        print('finding the Microsoft button')
        microsoft = await tab.find("Microsoft", best_match=True)

        print('"Microsoft" => click')
        await microsoft.click()

        print("finding the email input field")
        email = await tab.select("input[type=email]")

        print('filling in the "email" input field')
        await email.send_keys("pranjal_2302cs06@iitp.ac.in")

        print('finding the Next button')
        next = await tab.find("Next", best_match=True)

        print('"Next" => click')
        await next.click()

        print("finding the password input field")
        password = await tab.select("input[type=password]")

        print('filling in the "password" input field')
        await password.send_keys("easypass123@")

        print("wait for the page to load")
        # TODO: read ms.js which uses knockoutjs and figure out which function primaryButton_onClick refers to
        await tab.wait(1)

        print('finding the "Sign in" button')
        Sign_in = await tab.select("input[type=submit]")
        await Sign_in.click()

        print("wait for the page to load")
        await tab.wait(2)
        await driver.cookies.save()
    except:
        pass

    #print('"Sign in" => click')
    #await Sign_in.click()

#    await tab.select('body')
#    await tab.get("https://ais.iitp.ac.in/moodle/course/index.php?categoryid=846")
#    await tab.get("https://ais.iitp.ac.in/moodle/course/index.php?categoryid=864")
    Dashboard = await tab.find("Dashboard")
    await Dashboard.click()

    print('finding the "All courses" button')
    All_courses = await tab.find("All courses")

    print('"All courses" => click')
    await All_courses.click()

    await tab.wait(5)
#    Spring_Autumn_Registration_2025 = await tab.select("Spring-Autumn Registration-2025")
#    await Spring_Autumn_Registration_2025.click()

    e = await tab.find('Spring-Autumn Registration-2025 / B. Tech. Spring-Autumn Registration 2025 / Semester-V / Core Subjects / Computer Science &amp; Engineering', best_match=True)
    print(e)
    await tab.wait(10)
    await e.click()


    #Expand_All = await tab.find("Expand All", best_match=True)
    #await Expand_All.click()
   # text = await tab.get_all_urls()
    #print(text)
#    await tab.wait_for("input[type=text]")
#    text = await tab.select("input[type=text]")
#    await text.send_keys("CE 3105:")
#    Search_courses = await tab.find("Search courses")
#    await Search_courses.click()

#    "Spring-Autumn Registration-2025 / B. Tech. Spring-Autumn Registration 2025 / Semester-V / IDE-II (Enroll in any one Course)"
#    "B. Tech. Spring-Autumn Registration 2025"
#    Semester_V = await tab.find("Semester-V", best_match=True)
#    await Semester_V.click()
#     IDE_II = tab.find("IDE-II (Enroll in any one Course)", best_match=True)
#    Core = await tab.find("Core", best_match=True)
#    await Core.click()
    #"CE 3105"

    time.sleep(900)

if __name__ == '__main__':
    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())
