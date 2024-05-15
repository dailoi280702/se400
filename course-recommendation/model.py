# class CourseRecommendationModel:
#
#     def __init__(self):
#         # ... (model architecture definition)
#         self.isTraining = False
#         return self
#
#     @staticmethod
#     def load_from_file(path):
#         # ... (load model from file)
#         model = CourseRecommendationModel()
#         return model
#
#     def predict(self, user_history_ids):
#         # ... (implement prediction logic)
#         return []
#
#     def save_to_file(self, path):
#         # ... (save model to file)
#         pass
#
#     def train(self):
#         self.isTraining = True
#
#         # data is located at data/processed_data.csv with bellow example data:
#         # id,name,university_name,difficulty_level,rating,description,skills_covered,instructor_name
#         # 4361,Write A Feature Length Screenplay For Film Or Television,Michigan State University,Beginner,4.8,"Write a Full Length Feature Film Script  In this course, you will write a complete, feature-length screenplay for film or television, be it a serious drama or romantic comedy or anything in between. You�ll learn to break down the creative process into components, and you�ll discover a structured process that allows you to produce a polished and pitch-ready script by the end of the course. Completing this project will increase your confidence in your ideas and abilities, and you�ll feel prepared to pitch your first script and get started on your next. This is a course designed to tap into your creativity and is based in ""Active Learning"". Most of the actual learning takes place within your own activities - that is, writing! You will learn by doing.  Here is a link to a TRAILER for the course. To view the trailer, please copy and paste the link into your browser. https://vimeo.com/382067900/b78b800dc0  Learner review: ""Love the approach Professor Wheeler takes towards this course. It's to the point, easy to follow, and very informative! Would definitely recommend it to anyone who is interested in taking a Screenplay Writing course!  The course curriculum is simple: We will adopt a professional writers room process in which you�ll write, post your work for peer review, share feedback with your peers and revise your work with the feedback you receive from your peers. That's how we do it in the real world. You will feel as if you were in a professional writers room yet no prior experience as a writer is required. I'm a proponent of Experiential Learning (Active Learning). My lectures are short (sometimes just two minutes long) and to the point, designed in a step-by-step process essential to your success as a script writer. I will guide you but I won�t ""show"" you how to write. I firmly believe that the only way to become a writer is to write, write, write.  Learner Review: ""I would like to thank this course instructor. It's an amazing course""  What you�ll need to get started: As mentioned above, no prior script writing experience is required. To begin with, any basic word processor will do. During week two, you can choose to download some free scriptwriting software such as Celtx or Trelby or you may choose to purchase Final Draft, the industry standard, or you can continue to use your word processor and do your own script formatting.   Learner Review: ""Now I am a writer!""  If you have any concerns regarding the protection of your original work, Coursera's privacy policy protects the learner's IP and you are indeed the sole owners of your work.",Drama  Comedy  peering  screenwriting  film  Document Review  dialogue  creative writing  Writing  unix shells arts-and-humanities music-and-art,
#
#         # skills_covered is similar to categories
#
#         # ... (implement training logic)
#
#         self.isTraining = False
#         pass


# import torch
# from torch import nn
# from torch.utils.data import Dataset, DataLoader
#
# class Course(object):
#     def __init__(self, id, name, rating, skills_covered):
#         self.id = id
#         self.name = name
#         self.rating = rating
#         self.skills_covered = skills_covered  # Can be skill IDs or text
#
# class CourseDataset(Dataset):
#     def __init__(self, data_path):
#         self.courses = []
#         # Load data from CSV file (replace with your actual loading logic)
#         with open(data_path, "r") as f:
#             # Skip header row (if present)
#             next(f)
#             for line in f:
#                 # Parse data into Course objects
#                 data = line.strip().split(",")
#                 course_id, name, _, _, rating, _, _, _ = data[:8]
#                 skills = data[8].split(" ")  # Assuming skills are space-separated
#                 self.courses.append(Course(int(course_id), name, float(rating), skills))
#
#     def __len__(self):
#         return len(self.courses)
#
#     def __getitem__(self, idx):
#         return self.courses[idx]
#
# class CourseRecommendationModel(nn.Module):
#     def __init__(self, num_users, num_courses, latent_dim, embedding_dim, num_skills):
#         super(CourseRecommendationModel, self).__init__()
#         self.user_embeddings = nn.Embedding(num_users, latent_dim)
#         self.course_embeddings = nn.Embedding(num_courses, embedding_dim)
#         self.skill_embeddings = nn.Embedding(num_skills, embedding_dim)
#         self.mlp = nn.Sequential(
#             nn.Linear(latent_dim + embedding_dim + embedding_dim, hidden_dim),
#             nn.ReLU(),
#             nn.Linear(hidden_dim, 1),  # Output layer for interaction probability
#         )
#
#     def forward(self, user_id, course_id):
#         user_factor = self.user_embeddings(user_id)
#         course_embedding = self.course_embeddings(course_id)
#
#         # Get skill embeddings for the course
#         skill_embeddings = [self.skill_embeddings(skill_id) for skill_id in skills_covered]
#         avg_skill_embedding = torch.mean(torch.stack(skill_embeddings), dim=0)
#
#         combined_features = torch.cat((user_factor, course_embedding, avg_skill_embedding), dim=1)
#         interaction_prob = self.mlp(combined_features)
#         return interaction_prob.squeeze()  # Remove extra dimension for single output
#
#     # ... other methods (load_from_file, save_to_file)
#
#     def train(self, train_data_path, epochs, learning_rate, augment_data=False):
#         self.isTraining = True
#
#         # Load training data
#         train_dataset = CourseDataset(train_data_path)
#         train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
#
#         # Define optimizer and loss function
#         optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
#         loss_fn = nn.BCELoss()
#
#         # Training loop
#         for epoch in range(epochs):
#             for user_ids, course_ids, ratings in train_loader:
#                 # Convert ratings to binary interaction labels (optional)
#                 interactions = (ratings >= threshold).float()  # Adjust threshold as needed
#
#                 # Forward pass
#                 predicted_probs = self(user_ids, course_ids)
#                 loss = loss_fn(predicted_probs, interactions)
#
#                 # Backward pass and parameter update
#                 optimizer.zero_grad()
#                 loss.backward()
#                 optimizer.step()
#
#             # Optional data augmentation for user-skill interactions (if enabled)
#             if augment_data:
#                 for user_id, course in train_dataset.courses:
#                     for skill in course.skills_covered:
#                         # Create additional training data point (user, skill)
#                         user_skill_interaction = (user_id, skill)
#                         # ... (implement logic to add user_skill_interaction to training data)
#
#             # Print training progress (optional)
#             print(f"Epoch: {epoch+1}/{epochs}, Loss:

import torch
from torch import nn
from torch.utils.data import Dataset


# Define the Course class to hold course information
class Course:
    def __init__(self, id, rating, difficulty_level, categories):
        self.id = id
        self.rating = rating
        self.difficulty_level = difficulty_level
        self.categories = categories


# Create a custom dataset class to load and process data
class CourseRecommendationDataset(Dataset):
    def __init__(self, data_path):
        self.courses = []
        # Load data from CSV file
        with open(data_path, "r") as f:
            # Skip header row
            next(f)
            for line in f:
                data = line.strip().split(",")
                # Extract relevant features
                id = int(data[0])
                difficulty_level = data[1]
                rating = float(data[2])
                categories = data[3].split(" ")  # Split categories string
                self.courses.append(Course(id, rating, difficulty_level, categories))
        print(f"Dataset loaded: {len(self.courses)} lines")

    def __len__(self):
        return len(self.courses)

    def __getitem__(self, idx):
        return self.courses[idx]


# Define the CourseRecommendationModel class
class CourseRecommendationModel(nn.Module):
    def __init__(self, embedding_dim, hidden_dim, dataset):
        super(CourseRecommendationModel, self).__init__()
        self.courses = dataset.courses
        num_courses = len(set([course.id for course in dataset.courses]))

        # Embedding layer for categorical features (difficulty level and categories)
        self.difficulty_embedding = nn.Embedding(
            num_embeddings=len(
                set([course.difficulty_level for course in self.courses])
            ),
            embedding_dim=embedding_dim,
        )
        self.category_embedding = nn.Embedding(
            num_embeddings=len(
                set(
                    [
                        category
                        for course in self.courses
                        for category in course.categories
                    ]
                )
            ),
            embedding_dim=embedding_dim,
        )
        # Input layer for rating
        self.rating_input = nn.Linear(1, embedding_dim)
        # Combine embeddings and rating
        self.embedding_cat = nn.Linear(
            embedding_dim * 2, hidden_dim
        )  # After embedding difficulty and categories
        self.embedding_all = nn.Linear(
            embedding_dim + hidden_dim, hidden_dim
        )  # After combining rating with embeddings
        # Layers for prediction
        self.hidden1 = nn.Linear(hidden_dim, hidden_dim)
        self.output = nn.Linear(hidden_dim, num_courses)

    def forward(self, user_history_ids):
        # Get courses based on user history IDs
        user_history_courses = [
            course for course in self.courses if course.id in user_history_ids
        ]

        # Embed difficulty level and categories
        difficulty_embeddings = self.difficulty_embedding(
            [course.difficulty_level for course in user_history_courses]
        )
        category_embeddings = torch.zeros(
            (
                len(user_history_courses),
                len(user_history_courses[0].categories),
                self.embedding_dim,
            )
        )
        for i, course in enumerate(user_history_courses):
            for j, category in enumerate(course.categories):
                category_embeddings[i][j] = self.category_embedding(category)
        # Average category embeddings
        category_embeddings = torch.mean(category_embeddings, dim=1)

        # Combine embeddings
        difficulty_and_category_embeddings = torch.cat(
            (difficulty_embeddings, category_embeddings), dim=1
        )
        embedded_difficulty_and_categories = self.embedding_cat(
            difficulty_and_category_embeddings
        )

        # Embed rating
        rating_embeddings = self.rating_input(
            torch.tensor([course.rating for course in user_history_courses]).unsqueeze(
                1
            )
        )

        # Combine all features
        combined_embeddings = torch.cat(
            (embedded_difficulty_and_categories, rating_embeddings), dim=1
        )
        embedded_all = self.embedding_all(combined_embeddings)

        # Hidden layer and output
        hidden1_out = self.hidden1(embedded_all)
        output = self.output(hidden1_out)
        return output

    def load_from_file(self, path):
        # Load model state and courses from file
        torch.save(self.state_dict(), path)
