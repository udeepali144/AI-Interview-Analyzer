class AIInterviewer:

    def __init__(self, questions):

        # Questions ko list me convert karo
        if isinstance(questions, dict):

            question_list = []

            for value in questions.values():

                if isinstance(value, list):

                    question_list.extend(value)

                else:

                    question_list.append(value)

            self.questions = question_list

        else:

            self.questions = questions

        self.current_index = 0
        self.last_score = None
        self.asked_questions = []

    # -----------------------------------------
    # CURRENT QUESTION
    # -----------------------------------------

    def get_current_question(self):

        if self.current_index < len(self.questions):

            question = self.questions[
                self.current_index
            ]

            if question not in self.asked_questions:

                self.asked_questions.append(
                    question
                )

            return question

        return None

    # -----------------------------------------
    # ADAPTIVE QUESTION
    # -----------------------------------------

    def get_adaptive_question(self, score):

        self.last_score = score

        # Difficulty decide karo

        if score < 60:

            difficulty = "Easy"

        elif score < 80:

            difficulty = "Medium"

        else:

            difficulty = "Hard"

        # Matching unused question find karo

        for index, question in enumerate(
            self.questions
        ):

            if isinstance(question, dict):

                if (
                    question.get("difficulty")
                    == difficulty
                    and question not in self.asked_questions
                ):

                    return index

        return None

    # -----------------------------------------
    # NEXT QUESTION
    # -----------------------------------------

    def next_question(self, score=None):

        self.last_score = score

        # Adaptive question try karo

        if score is not None:

            adaptive_index = self.get_adaptive_question(
                score
            )

            if adaptive_index is not None:

                self.current_index = adaptive_index

                return self.get_current_question()

        # Normal next question

        self.current_index += 1

        return self.get_current_question()

    # -----------------------------------------
    # CHECK FINISHED
    # -----------------------------------------

    def has_finished(self):

        return self.current_index >= len(
            self.questions
        )

    # -----------------------------------------
    # RESET
    # -----------------------------------------

    def reset(self):

        self.current_index = 0
        self.last_score = None
        self.asked_questions = []