package redisC

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
)

type RedisC struct {
	C *redis.Client
}

var RDB *RedisC

func init() {
	c := redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "",
		DB:       0,
	})
	RDB = &RedisC{C: c}

	if err := RDB.C.Ping(context.Background()).Err(); err != nil {
		log.Println(err)
	}

	log.Println("Redis connected")
}

func (r *RedisC) SetJSON(key string, value any, expiration time.Duration) error {
	p, err := json.Marshal(value)
	if err != nil {
		return err
	}

	return r.C.Set(context.Background(), key, p, expiration).Err()
}

func (r *RedisC) GetJSON(key string, dest any) error {
	p, err := r.C.Get(context.Background(), key).Result()
	if err != nil {
		return err
	}

	return json.Unmarshal([]byte(p), dest)
}
