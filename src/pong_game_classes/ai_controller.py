class AIController:

    @staticmethod
    def return_decision(ai_difficulty:str, ball_trajectory_snapshot:dict, paddle_position:dict, game_dt:float) -> str:
        if ai_difficulty == "hard":
            return AIController._predictive_tracking_decision(ball_trajectory_snapshot, paddle_position, game_dt)
        return AIController._simple_tracking_decision(ball_trajectory_snapshot, paddle_position)

    @staticmethod    
    def _predictive_tracking_decision(ball_trajectory_snapshot:dict, paddle_position:dict, game_dt:float) -> str:
        """Logic: Predict where the ball will cross the ai's paddle x-coordinate, by taking into consideration:
            - current ball trajectory
            - anticipated reflection(s)
            Respond by moving the paddle in the direction corresponding with the predicted calculation.
            
            Parameter(s): 
                - ball_trajectory_snapshot (dict)
                {
                    "x_position": float               
                    "y_position": float                 
                    "x_velocity": float         
                    "y_velocity": float         
                    "x_direction": int
                    "y_direction": int
                    "lower_reflection_bound": int   
                    "upper_reflection_bound": int
                }
                - paddle_position (dict):
                {
                    "x": int
                    "y": int
                    "height": float
                }    
        """
        time_to_cross_x_threshold: float = abs((paddle_position["x"] - ball_trajectory_snapshot["x_position"]) / ball_trajectory_snapshot["x_velocity"])

        ball_y_pos_predicted: int = ball_trajectory_snapshot["y_position"]              # set to current y-position
        ball_y_velocity_calculated: float = ball_trajectory_snapshot["y_velocity"]      # set to current y-velocity

        time_left: float = time_to_cross_x_threshold                                    # initialize to time for ball to cross x pos of paddle

        while time_left > 0:
            time_step = min(game_dt, time_left)
            ball_y_pos_predicted += ball_y_velocity_calculated * time_step

            lower_screen_collision = ball_y_pos_predicted >= ball_trajectory_snapshot["lower_reflection_bound"] 
            if lower_screen_collision:
                ball_y_pos_predicted = ball_trajectory_snapshot["lower_reflection_bound"] - (ball_y_pos_predicted - ball_trajectory_snapshot["lower_reflection_bound"])
                ball_y_velocity_calculated *= -1

            upper_screen_collision = ball_y_pos_predicted <= ball_trajectory_snapshot["upper_reflection_bound"]
            if upper_screen_collision:
                ball_y_pos_predicted = ball_trajectory_snapshot["upper_reflection_bound"] + (ball_trajectory_snapshot["upper_reflection_bound"] - ball_y_pos_predicted)
                ball_y_velocity_calculated *= -1
     
            time_left -= time_step
        
        if ball_y_pos_predicted < paddle_position["y"] + (paddle_position["height"]*0.5): return "move_up"
        elif ball_y_pos_predicted > paddle_position["y"] + (paddle_position["height"]*0.5): return "move_down"
        else: return "stay"
    
    @staticmethod
    def _simple_tracking_decision(ball_trajectory_snapshot:dict, paddle_position:dict) -> str:
        """
            Simply instructs the paddle;s movement based on checking ball's y-position relation to the paddle's y-position.
        """
        result: str = "stay"
        if ball_trajectory_snapshot["x_direction"] == 1:
            if ball_trajectory_snapshot["y_position"] < paddle_position["y"] + (paddle_position["height"]*0.5): result = "move_up"
            elif ball_trajectory_snapshot["y_position"] > paddle_position["y"] + (paddle_position["height"]*0.5): result = "move_down"
        return result