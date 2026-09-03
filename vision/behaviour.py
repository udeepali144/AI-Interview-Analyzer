class BehaviourTracker:

    def __init__(self):

        self.total_frames = 0

        self.face_frames = 0
        self.eye_contact_frames = 0
        self.head_center_frames = 0
        self.upright_frames = 0

    def update(
        self,
        face_detected,
        eye_contact,
        head_center,
        upright
    ):

        self.total_frames += 1

        if face_detected:
            self.face_frames += 1

        if eye_contact:
            self.eye_contact_frames += 1

        if head_center:
            self.head_center_frames += 1

        if upright:
            self.upright_frames += 1

    def percentage(self, value):

        if self.total_frames == 0:
            return 0.0

        return round(
            (value / self.total_frames) * 100,
            2
        )

    def get_report(self):

        return {

            "face_presence":
                self.percentage(
                    self.face_frames
                ),

            "eye_contact":
                self.percentage(
                    self.eye_contact_frames
                ),

            "head_stability":
                self.percentage(
                    self.head_center_frames
                ),

            "upright_posture":
                self.percentage(
                    self.upright_frames
                )
        }