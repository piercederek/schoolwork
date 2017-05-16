package com.jadeinc.habitracker;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Created by evan on 4/20/17.
 */

@JsonIgnoreProperties(ignoreUnknown = true)
public class Task {
    private String task;
    private String time;
    private String frequency;
    private int timeCompleted;
    private long daySec = 86400;

    public int bestStreak;
    public int currentStreak;

    public Task() {}

    public Task(String task) {
        this.task = task;
    }

    public String getTask() {
        return task;
    }
    public void setTask(String task) {
        this.task = task;
    }

    public String getTime() { return this.time;}
    public void setTime(String time) { this.time = time;}

    public String getFrequency() { return this.frequency; }
    public void setFrequency(String frequency) { this.frequency = frequency; }

    public int getTimeCompleted() {return this.timeCompleted;}

    public void setTimeCompleted(String timeCompleted) {this.timeCompleted = Integer.parseInt(timeCompleted);}
    public void setTimeCompleted(int timeCompleted) {this.timeCompleted = timeCompleted;}


    public void complete() {
        int now = (int) (System.currentTimeMillis() / 1000);
        this.setTimeCompleted(now);
        currentStreak++;
        bestStreak = Math.max(currentStreak, bestStreak);
    }

    public boolean isCompleted() {
        long currTime = System.currentTimeMillis() / 1000;
        if (timeCompleted == 0) {
            return false;
        }
        if (currTime - daySec <= timeCompleted) {
            return true;
        }
        return false;
    }

    @Override
    public String toString() {
        return this.task;
    }
}
