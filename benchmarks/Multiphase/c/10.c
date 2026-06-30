int main(){
    int x;

    // pre-conditions
    x = 0;

    // loop body
    while(unknown()){
        if(x / 5 < 200){
            x = x + 1;
        }else{
            x = x + 5;
        }
    }

    // post-condition
    if(x >= 2000){
        assert(x % 5 == 0);
    }
    
}