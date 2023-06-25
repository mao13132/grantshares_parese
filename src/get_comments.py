from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.filter_date import FilterDate


class GetComments:
    def __init__(self, driver):
        self.driver = driver

    def load_page(self, url):
        try:

            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на "{url}" "{es}"')
            return False

    def __check_load_page(self, name_post):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{name_post[:-3]}")]')))
            return True
        except Exception as es:
            print(f'Ошибка при загрузке "{name_post}" поста "{es}"')
            return False

    def loop_load_page(self, post):
        coun = 0
        coun_ower = 10

        while True:
            coun += 1

            if coun >= coun_ower:
                print(f'Не смог зайти в пост {post["name_post"]}')
                return False

            response = self.load_page(post['link_git'])

            if not response:
                continue

            result_load = self.__check_load_page(post['name_post'])

            if not result_load:
                self.driver.refresh()
                return False

            return True

    def get_all_comments(self):

        try:

            rows_comm = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, "
                                                                     f"'timeline-progressive-focus-container')]")

        except:

            return []

        return rows_comm

    def get_author_comment(self, comm):
        try:
            author_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'author')]").text

        except:
            author_comment = ''

        return author_comment

    def get_date_comment(self, comm):
        try:
            date_comment = comm.find_element(by=By.TAG_NAME, value=f"relative-time").get_attribute('datetime')

        except:
            date_comment = ''

        return date_comment

    def get_text_comment(self, comm):
        try:
            text_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'user-select-contain')]").text

        except:
            text_comment = ''

        return text_comment

    def get_likes_comments(self, comm):
        try:
            likes_comment = comm.find_element(by=By.XPATH,
                                              value=f".//*[contains(@class, 'comment-reactions')]"
                                                    f"//span[contains(@class, 'count')]").text

        except:
            return 0

        return likes_comment

    def itter_rows_comm(self, rows_comm, post):

        comments_list = []

        for comm in rows_comm[1:]:
            comment_dict = {}

            author_comment = self.get_author_comment(comm)
            if author_comment == '':
                continue

            comment_dict['author_comment'] = author_comment

            time_comment = self.get_date_comment(comm)
            comment_dict['date_comment'] = FilterDate.get_format(time_comment).strftime('%d.%m.%Y')

            text_comment = self.get_text_comment(comm)
            comment_dict['text_comment'] = text_comment

            like = self.get_likes_comments(comm)
            comment_dict['like_comment'] = like

            comments_list.append(comment_dict)

        post['comments'].extend(comments_list)

        return True

    def job_comments(self, post):
        post['comments'] = []

        rows_comm = self.get_all_comments()

        if rows_comm == []:
            return True

        response_itter = self.itter_rows_comm(rows_comm, post)

        # print()

    def start(self, post):

        result_load_page = self.loop_load_page(post)

        list_comments = self.job_comments(post)

        # print()


if __name__ == '__main__':
    from browser.createbrowser import CreatBrowser

    browser_core = CreatBrowser()

    post = {'id': '56e376ae5fc02922f484822665ff2015', 'name_post': 'Learn-to-Earn Education bot by MelkDAO',
            'date_post': '10.05.23', 'link': 'https://grantshares.io/app/details/56e376ae5fc02922f484822665ff2015',
            'link_git': 'https://github.com/AxLabs/grantshares/issues/82', 'name_them': 'request-for-funding',
            'step': 'Accepted',
            'text_post': "Abstract\nLearn-to-Earn is a teaching methodology that incentivizes individuals to acquire knowledge. At MELK DAO, we have developed a Discord bot that enables users to learn at their own pace, complete on-chain missions and engage with the Web3 ecosystem using $MELK tokens. Our proposed project involves creating a trail mission for the NEO ecosystem and the aim is to onboard new users and encourage them to explore and utilize the full potential of the NEO ecosystem, while earning rewards for their efforts. At MELK DAO, we believe that learning about the Web3 ecosystem should be engaging and rewarding. Our Learn-to-Earn methodology is designed to make learning fun and accessible, regardless of the level of experience.\nProposal Information\nDescription\nOur project is focused on creating a trail of missions for the NEO ecosystem that aims to onboard new users and encourage them to explore and utilize the full potential of the NEO blockchain. By completing various missions, such as creating a NEO wallet, funding it, transferring NEO, exploring the blockchain, etc… users can gain a deeper understanding and proficiency in using the NEO blockchain.\nOur trail mission is designed to be simple and user-friendly, providing step-by-step instructions and guidance for users who are new to the NEO ecosystem. To incentivize user participation and engagement, we offer rewards for completing each mission, such as MELK tokens or other tokens and assets. In addition, we have also created a Proof of Knowledge certificate that might provide reputation status and additional benefits to the community members who have completed the trail missions.\nThrough our project, we aim to onboard new users to the NEO ecosystem and encourage them to become active members of the community, contributing to the growth and development of the NEO blockchain. By unlocking the full potential of the NEO ecosystem, users can benefit from enhanced security, privacy, and reliability, and access various applications and services available on the platform.\nOur current MVP for Ethereum onboarding is already installed and running in 10 different servers with a reach of 10'000 users and 15% organic conversion in the past 6 months. More details can be found in our documentation here: https://docs.melkdao.com/v/en/\nMotivation\nOur goal is to onboard millions of individuals into the Web3 ecosystem, and we are searching for products and ecosystems that create a meaningful impact in the space. We strongly believe that NEO is one such ecosystem that has tremendous potential to make a significant contribution to the Web3 community.\nCurrently, our founding team is working on a voluntary basis, sharing the same vision and passion of promoting the Web3 ecosystem and its potential benefits. However, we recognize that additional resources are needed to bring these developments to life. Therefore, we are seeking grants as a means to support the development of this project and help achieve our mission.\nGoals\nWhat are the main goals, and why?\nThe main goal of our project is to create the first part of a trail mission for the NEO ecosystem that aims to onboard new users and encourage them to explore and utilize the full potential of the NEO blockchain. By completing various missions related to the NEO blockchain, users can gain a deeper understanding and proficiency in using the platform. The reason for this goal is to increase and maximize the adoption and usage of the NEO blockchain and products.\nThrough our project, we aim to amplify and simplify the process of onboarding new users to the NEO ecosystem by providing step-by-step instructions and guidance.\nHow would you bring value to the community?\nOverall we aim to bring more users, engagement and collaboration to NEO. Here's how:\nOnboarding new users: By creating a trail mission that provides step-by-step guidance and incentives for completing various missions related to the NEO blockchain, we can help onboard new users and increase the adoption and usage of the platform.\nPromoting community engagement: By offering rewards for completing missions and providing opportunities for participation and collaboration, our project can help foster a strong and engaged community of developers, investors, and users around the NEO blockchain.\nEnhancing awareness: By promoting the adoption and usage of the NEO blockchain through our project, we can raise awareness of the platform and its unique features, which can help attract new users, developers, and investors to the NEO community.\nDeliverables & Roadmap\nHere's what the first phase of our deliverables include:\nResearch and Planning:\nDuration: 1 week\nResearch the NEO ecosystem, define the trail mission objectives, and create a detailed project plan.\nSmart Contract Development:\nDuration: 2 weeks\nCreate and deploy new smart contracts for each mission in the trail. These smart contracts will manage user actions, validate inputs, and trigger rewards upon completion of each mission.\nStaging and Debugging:\nDuration: 1 week\nTest and debug the smart contracts in a staging environment to ensure that the trail mission is functional and error-free.\nInterface Design and Development:\nDuration: 1 week\nDesign and develop a user-friendly interface for completing each mission in the trail. The interface will be easy to use and understand for both new and experienced users.\nReward System Development:\nDuration: 1 week\nDevelop a reward system that will incentivize users to complete each mission and earn rewards. This reward system will be integrated with the NEO blockchain to ensure that rewards are distributed automatically upon completion of each mission.\nSecurity and Vulnerability Testing:\nDuration: 1 week\nConduct security and vulnerability testing of the trail mission before and after deployment to ensure that it is secure and protected from potential attacks.\nStaging and Deployment:\nDuration: 1 week\nStage and deploy the trail mission to the NEO blockchain. Staging involves testing the trail mission in a production-like environment, while deployment involves deploying the trail mission to the NEO blockchain for users to access and complete.\nTotal FTE estimation for the project : 2\nTotal budget requested: ~6'670 GAS / 15'000 USD [Jun 12th]\nOnce the first phase is delivered we aim to expand the missions and introduce videos to support the learning path.\nDeliverables Verifiability\nPreviously, we developed and tested a trail mission for onboarding users into the EVM blockchain ecosystem. This served as our MVP to test the contract and understand its traction with users. The content for the trail mission is available for anyone to test on one of our servers with the bot installed. For more information, please refer to our documents here: https://docs.melkdao.com/v/en/comunidade.\nThe trail mission includes the following nine missions:\nCreating a wallet using MetaMask\nConfiguring a new network and a new token in your wallet\nViewing transactions on the blockchain\nUnderstanding the transaction information on the blockchain\nSigning transactions with MetaMask\nLearning to purchase MATIC\nLearning to swap tokens\nLearning to make transfers\nLearning to sign a Snapshot vote\nTo ensure transparency, the community will have access to our public GitHub page, where they can view the codebase and track the development progress. We will also provide regular updates through our Discord server to keep the broader community informed about the project's progress.\nBudget Plan\nWhat are the overall required resources (i.e., budget)?\nThe overall required resources for the development of the trail mission for the NEO ecosystem are approximately $15,000 USD. This budget will cover the costs of smart contract development, interface design and development, reward system development, security and vulnerability testing, and staging and deployment. The majority of the budget will be allocated towards development costs.\nProvide reasons why the requested budget is a good fit for the proposal.\nThe requested budget is a good fit for the proposal because it covers all the necessary development costs for creating a successful trail mission for the NEO ecosystem. Smart contract development will ensure that the trail mission is fully integrated with the NEO blockchain and functions as intended. Interface design and development will create a user-friendly experience for completing each mission in the trail. Reward system development will incentivize users to complete each mission and earn rewards. Security and vulnerability testing will ensure that the trail mission is secure and protected from potential attacks. Staging and deployment will ensure that the trail mission is ready for use by the NEO community.\nHow the budget would be used to achieve the project goal?\nThe budget will be used to achieve the project goal by covering the costs of the various deliverables required for the development of the trail mission.\nAbout You / Your Organization\nIndividual/Entity Name: MelkDAO\nWebsite: https://docs.melkdao.com/v/en/\nGitHub Organization (if applicable): https://github.com/web3melk/melk-dao-docs\nShort-Bio\nOur team:\nOur team is a group of talented individuals who are passionate about Web3 and blockchain technology. We have diverse backgrounds and expertise, ranging from entrepreneurship and venture capital to software development, project management, marketing, design, community growth, finance and business strategy.\nTogether, we are dedicated to creating innovative and meaningful onboarding experiences for Web3 ecosystem. Our team is driven by a shared vision of building a decentralized future that is more secure, transparent, and accessible to everyone.\nAbout us:\nWho we are : Creators of the world's first on chain Learn-to-Earn Discord bot!\nWhat we do :We democratize Web3 education through meaningful learning experiences.\nBenefits : Our learning methodology is effective and incentivize users to keep progressing.\nOur mission: Onboard millions of people into Web3 ecosystem.\nPortfolio of Projects / Past Experience\nTeam roles and experience:\nAna/Purple , Co-Founder & General Manager: Ana, aka Purple in Web3 is an ex-P&G with vast experience in F&A and market research. Now leads community growth and strategy for innovative blockchain products at ConsenSys.\nRai, Co-Founder & Marketing Manager: Rai is a Web3 educator and digital content creator with 10+ years of experience in project management and marketing.\nLorenzo, Co-Founder & Developer: Lorenzo is a skilled software developer with relevant experience in blockchain development and web projects.\nAkva, Co-Founder & Community Builder: Akva is an experienced Web3 degen who has been part of important founding teams in Brazil. He has extensive experience with building engaged communities.\nDesenhista, Co-Founder & Illustrator: Desenhista is a talented digital artist, recognized in the Brazilian community for creating fun and pixeled artwork. In his spare time, he practices law.\nMelk, Co-Founder & Advisor: Melk is a founder with a diverse background in entrepreneurship, venture capital, fintech, and Web3. He now contributes as the main advisor for MelkDAO.\nSome of the projects that the team has been involved:\nweb3dev: https://www.web3dev.com.br/\nOn-demand web3 software development.\nBrPunk community: https://brpunk.com/\nDecentralized persona creating and curating Web3 content\nnounsbr: https://nounsbr.com/en/\nAn extension of Nouns DAO, which seeks to introduce Nouns in the various cultural manifestations that give identity and tell the history of Brazil.\nHoneyBadgers: https://twitter.com/HoneyBadgersBtc\ndigital collectibles inscribed on the Bitcoin Blockchain. First Badger: #81.557 Last Badger: #1.014.824",
            'name_author': 'PurpleRatatui', 'voting_starts': '13.06.2023 17:40', 'voting_end': '20.06.2023 17:40',
            'get_funding': '6670', 'voting_yes': '4', 'voting_no': '0', 'voting_abstain': '1'}

    res = GetComments(browser_core.driver).start(post)

    print()
